from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    year,
    unix_timestamp
)
import glob

# =====================================================
# CREATE SPARK SESSION
# =====================================================

spark = (
    SparkSession.builder
    .appName("NYC Taxi Category A Cleaning")
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

dfs = []

for file in parquet_files:

    print(f"Loading: {file}")

    temp_df = spark.read.parquet(file)

    if "passenger_count" in temp_df.columns:
        temp_df = temp_df.withColumn(
            "passenger_count",
            col("passenger_count").cast("double")
        )

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

df = dfs[0]

for temp_df in dfs[1:]:

    df = df.unionByName(
        temp_df,
        allowMissingColumns=True
    )

print("\nDatasets Combined Successfully")

# =====================================================
# INITIAL CLEANING
# =====================================================

df = (
    df
    .filter(col("passenger_count") > 0)
    .filter(
        year("tpep_pickup_datetime").between(2021, 2026)
    )
)

print("\nInitial Cleaning Applied")

# =====================================================
# CREATE TRIP DURATION
# =====================================================

df = df.withColumn(
    "trip_duration_min",
    (
        unix_timestamp("tpep_dropoff_datetime")
        -
        unix_timestamp("tpep_pickup_datetime")
    ) / 60
)

# =====================================================
# CATEGORY A COUNTS
# =====================================================

negative_distance_count = df.filter(
    col("trip_distance") < 0
).count()

negative_tip_count = df.filter(
    col("tip_amount") < 0
).count()

negative_duration_count = df.filter(
    col("trip_duration_min") < 0
).count()

duration_over_24h_count = df.filter(
    col("trip_duration_min") > 1440
).count()

distance_over_10000_count = df.filter(
    col("trip_distance") > 10000
).count()

# =====================================================
# CATEGORY A CLEANING
# =====================================================

clean_df = df.filter(

    (col("trip_distance") >= 0)

    &

    (col("tip_amount") >= 0)

    &

    (col("trip_duration_min") >= 0)

    &

    (col("trip_duration_min") <= 1440)

    &

    (col("trip_distance") <= 10000)

)

# =====================================================
# SUMMARY
# =====================================================

original_count = df.count()
final_count = clean_df.count()

removed_count = original_count - final_count

print("\n======================================")
print("CATEGORY A CLEANING SUMMARY")
print("======================================")

print(f"Records Before Cleaning : {original_count:,}")
print(f"Records After Cleaning  : {final_count:,}")
print(f"Total Removed           : {removed_count:,}")

print("\nRemoved Records")

print(
    f"Negative Distance     : "
    f"{negative_distance_count:,}"
)

print(
    f"Negative Tip          : "
    f"{negative_tip_count:,}"
)

print(
    f"Negative Duration     : "
    f"{negative_duration_count:,}"
)

print(
    f"Duration > 24 Hours   : "
    f"{duration_over_24h_count:,}"
)

print(
    f"Distance > 10,000     : "
    f"{distance_over_10000_count:,}"
)

# =====================================================
# SAVE CLEAN DATASET
# =====================================================

clean_df.write.mode("overwrite").parquet(
    "artifacts/clean_category_A"
)

print("\nDataset Saved Successfully")

print(
    "\nOutput Location:"
    "\nartifacts/clean_category_A"
)

spark.stop()