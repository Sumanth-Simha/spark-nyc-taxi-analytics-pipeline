
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year
import glob

# =====================================================
# CREATE SPARK SESSION
# =====================================================

spark = (
    SparkSession.builder
    .appName("NYC Taxi Outlier Detection")
    .config("spark.driver.memory", "4g")
    .config("spark.executor.memory", "4g")
    .config("spark.sql.shuffle.partitions", "8")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

spark.conf.set(
    "spark.sql.parquet.enableVectorizedReader",
    "false"
)

print("\nSpark Session Created")

# =====================================================
# LOAD DATA
# =====================================================

parquet_files = sorted(glob.glob("data/*.parquet"))

print(f"\nFound {len(parquet_files)} parquet files.\n")

dfs = []

for file in parquet_files:

    print(f"Loading: {file}")

    temp_df = spark.read.parquet(file)

    # Standardize passenger_count
    if "passenger_count" in temp_df.columns:
        temp_df = temp_df.withColumn(
            "passenger_count",
            col("passenger_count").cast("double")
        )

    # Standardize timestamps
    if "tpep_pickup_datetime" in temp_df.columns:
        temp_df = temp_df.withColumn(
            "tpep_pickup_datetime",
            col("tpep_pickup_datetime").cast("timestamp")
        )

    if "tpep_dropoff_datetime" in temp_df.columns:
        temp_df = temp_df.withColumn(
            "tpep_dropoff_datetime",
            col("tpep_dropoff_datetime").cast("timestamp")
        )

    dfs.append(temp_df)

# =====================================================
# COMBINE DATASETS
# =====================================================

if len(dfs) == 0:
    raise Exception(
        "No parquet files found in data folder."
    )

df = dfs[0]

for temp_df in dfs[1:]:
    df = df.unionByName(
        temp_df,
        allowMissingColumns=True
    )

print("\nDatasets combined successfully.")

# =====================================================
# BASIC CLEANING
# =====================================================

cleaned_df = (
    df
    .filter(col("passenger_count") > 0)
    .filter(
        year("tpep_pickup_datetime").between(2021, 2026)
    )
)

print("\nBasic Cleaning Applied:")
print("- Removed passenger_count <= 0")
print("- Kept trips between 2021 and 2026")

print("\nTotal Trips After Cleaning:")
print(cleaned_df.count())

# =====================================================
# CALCULATE EXTREME PERCENTILES
# =====================================================

columns_to_check = [
    "fare_amount",
    "total_amount",
    "trip_distance",
    "tip_amount"
]

percentiles = {}

print("\n===================================")
print("PERCENTILE ANALYSIS")
print("===================================")

for column in columns_to_check:

    p99, p999 = cleaned_df.approxQuantile(
        column,
        [0.99, 0.999],
        0.001
    )

    percentiles[column] = {
        "99": p99,
        "99.9": p999
    }

    print(f"\n{column}")
    print(f"99th percentile   : {p99}")
    print(f"99.9th percentile : {p999}")

# =====================================================
# INSPECT EXTREME TOTAL AMOUNTS
# =====================================================

print("\n===================================")
print("TOP 20 TOTAL AMOUNTS")
print("===================================")

cleaned_df.select(
    "trip_distance",
    "fare_amount",
    "tip_amount",
    "total_amount"
).orderBy(
    col("total_amount").desc()
).show(20, truncate=False)

# =====================================================
# INSPECT EXTREME DISTANCES
# =====================================================

print("\n===================================")
print("TOP 20 TRIP DISTANCES")
print("===================================")

cleaned_df.select(
    "trip_distance",
    "fare_amount",
    "tip_amount",
    "total_amount"
).orderBy(
    col("trip_distance").desc()
).show(20, truncate=False)

# =====================================================
# INSPECT EXTREME TIPS
# =====================================================

print("\n===================================")
print("TOP 20 TIPS")
print("===================================")

cleaned_df.select(
    "trip_distance",
    "fare_amount",
    "tip_amount",
    "total_amount"
).orderBy(
    col("tip_amount").desc()
).show(20, truncate=False)

# =====================================================
# INVALID TRIPS
# =====================================================

invalid_df = cleaned_df.filter(

    (col("fare_amount") < 0)

    |

    (col("total_amount") < 0)

    |

    (col("trip_distance") < 0)

    |

    (
        (col("trip_distance") == 0)
        &
        (col("total_amount") > 100)
    )

    |

    (
        (col("fare_amount") == 0)
        &
        (col("total_amount") > 100)
    )
)

print("\n===================================")
print("INVALID TRIPS")
print("===================================")

print("Invalid Trip Count:")
print(invalid_df.count())

invalid_df.select(
    "trip_distance",
    "fare_amount",
    "tip_amount",
    "total_amount"
).show(20, truncate=False)

# =====================================================
# SUSPICIOUS TRIPS
# =====================================================

p999_total = percentiles["total_amount"]["99.9"]
p999_distance = percentiles["trip_distance"]["99.9"]

suspicious_df = cleaned_df.filter(

    (
        col("total_amount") > p999_total
    )

    |

    (
        col("trip_distance") > p999_distance
    )

    |

    (
        col("tip_amount") > col("fare_amount") * 5
    )
)

# Remove invalid trips from suspicious trips
suspicious_df = suspicious_df.subtract(invalid_df)

print("\n===================================")
print("SUSPICIOUS TRIPS")
print("===================================")

print("Suspicious Trip Count:")
print(suspicious_df.count())

suspicious_df.select(
    "trip_distance",
    "fare_amount",
    "tip_amount",
    "total_amount"
).show(20, truncate=False)

# =====================================================
# SAVE OUTPUTS
# =====================================================

invalid_df.write.mode("overwrite").parquet(
    "artifacts/invalid_trips"
)

suspicious_df.write.mode("overwrite").parquet(
    "artifacts/suspicious_trips"
)

print("\nOutputs Saved:")
print("- artifacts/invalid_trips")
print("- artifacts/suspicious_trips")

# =====================================================
# SUMMARY
# =====================================================

print("\n===================================")
print("SUMMARY")
print("===================================")

print("Original Trips   :", df.count())
print("Cleaned Trips    :", cleaned_df.count())
print("Invalid Trips    :", invalid_df.count())
print("Suspicious Trips :", suspicious_df.count())

print("\nOutlier Detection Completed Successfully.")

spark.stop()
