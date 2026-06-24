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
    .appName("NYC Taxi Extreme Investigation")
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

df = dfs[0]

for temp_df in dfs[1:]:
    df = df.unionByName(
        temp_df,
        allowMissingColumns=True
    )

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

print("\nCleaned Records:")
print(f"{cleaned_df.count():,}")

# =====================================================
# DISTANCE ANALYSIS
# =====================================================

print("\n====================================")
print("DISTANCE ANALYSIS")
print("====================================")

distance_thresholds = [50, 100, 500, 1000, 10000]

for threshold in distance_thresholds:

    count = cleaned_df.filter(
        col("trip_distance") > threshold
    ).count()

    print(
        f"Trips with distance > {threshold:>5}: "
        f"{count:,}"
    )

# =====================================================
# FARE ANALYSIS
# =====================================================

print("\n====================================")
print("FARE ANALYSIS")
print("====================================")

fare_thresholds = [200, 500, 1000, 5000, 10000]

for threshold in fare_thresholds:

    count = cleaned_df.filter(
        col("fare_amount") > threshold
    ).count()

    print(
        f"Trips with fare > ${threshold:>5}: "
        f"{count:,}"
    )

# =====================================================
# TOTAL AMOUNT ANALYSIS
# =====================================================

print("\n====================================")
print("TOTAL AMOUNT ANALYSIS")
print("====================================")

total_thresholds = [200, 500, 1000, 5000, 10000]

for threshold in total_thresholds:

    count = cleaned_df.filter(
        col("total_amount") > threshold
    ).count()

    print(
        f"Trips with total > ${threshold:>5}: "
        f"{count:,}"
    )

# =====================================================
# TIP ANALYSIS
# =====================================================

print("\n====================================")
print("TIP ANALYSIS")
print("====================================")

tip_thresholds = [100, 500, 1000]

for threshold in tip_thresholds:

    count = cleaned_df.filter(
        col("tip_amount") > threshold
    ).count()

    print(
        f"Trips with tip > ${threshold:>5}: "
        f"{count:,}"
    )

# =====================================================
# ZERO DISTANCE ANALYSIS
# =====================================================

print("\n====================================")
print("ZERO DISTANCE ANALYSIS")
print("====================================")

zero_distance = cleaned_df.filter(
    col("trip_distance") == 0
)

print(
    "Total zero-distance trips:",
    f"{zero_distance.count():,}"
)

print(
    "Zero distance + fare > 0:",
    f"{zero_distance.filter(col('fare_amount') > 0).count():,}"
)

print(
    "Zero distance + total > 0:",
    f"{zero_distance.filter(col('total_amount') > 0).count():,}"
)

# =====================================================
# DURATION ANALYSIS
# =====================================================

print("\n====================================")
print("DURATION ANALYSIS")
print("====================================")

duration_df = cleaned_df.withColumn(
    "trip_duration_min",
    (
        unix_timestamp("tpep_dropoff_datetime")
        -
        unix_timestamp("tpep_pickup_datetime")
    ) / 60
)

duration_checks = {
    "Negative Duration": col("trip_duration_min") < 0,
    "> 5 Hours": col("trip_duration_min") > 300,
    "> 10 Hours": col("trip_duration_min") > 600,
    "> 24 Hours": col("trip_duration_min") > 1440
}

for label, condition in duration_checks.items():

    count = duration_df.filter(
        condition
    ).count()

    print(f"{label:<20}: {count:,}")

# =====================================================
# TOP EXTREME RECORDS
# =====================================================

print("\n====================================")
print("TOP 50 DISTANCES")
print("====================================")

cleaned_df.select(
    "trip_distance",
    "fare_amount",
    "tip_amount",
    "total_amount"
).orderBy(
    col("trip_distance").desc()
).show(50, False)

print("\n====================================")
print("TOP 50 FARES")
print("====================================")

cleaned_df.select(
    "trip_distance",
    "fare_amount",
    "tip_amount",
    "total_amount"
).orderBy(
    col("fare_amount").desc()
).show(50, False)

print("\n====================================")
print("TOP 50 TOTALS")
print("====================================")

cleaned_df.select(
    "trip_distance",
    "fare_amount",
    "tip_amount",
    "total_amount"
).orderBy(
    col("total_amount").desc()
).show(50, False)

print("\nInvestigation Complete.")

spark.stop()