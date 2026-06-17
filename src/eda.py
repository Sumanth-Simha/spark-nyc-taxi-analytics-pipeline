from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, year, month, hour, count
)
from functools import reduce
import glob

# -------------------------
# Create Spark Session
# -------------------------
spark = (
    SparkSession.builder
    .appName("NYC Taxi EDA")
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

# -------------------------
# Load Data
# -------------------------
parquet_files = sorted(glob.glob("data/*.parquet"))

print(f"\nFound {len(parquet_files)} parquet files.\n")

dfs = []

for file in parquet_files:

    temp_df = spark.read.parquet(file)

    # Standardize passenger count
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

# -------------------------
# Combine Datasets
# -------------------------
df = reduce(
    lambda df1, df2: df1.unionByName(
        df2,
        allowMissingColumns=True
    ),
    dfs
)

# -------------------------
# Cleaning
# -------------------------
cleaned_df = (
    df
    .filter(col("passenger_count") > 0)
    .filter(
        year("tpep_pickup_datetime").between(2021, 2026)
    )
)

print("\nCleaning Applied:")
print("- Removed NULL passenger counts")
print("- Removed passenger_count <= 0")
print("- Removed trips outside 2021–2026")

# =====================================================
# YEARLY TRIP TRENDS
# =====================================================

print("\n====================================")
print("YEARLY TRIP TRENDS")
print("====================================")

yearly_trips = (
    cleaned_df
    .withColumn(
        "trip_year",
        year("tpep_pickup_datetime")
    )
    .groupBy("trip_year")
    .agg(count("*").alias("total_trips"))
    .orderBy("trip_year")
)

yearly_trips.show(truncate=False)

# =====================================================
# MONTHLY TRIP TRENDS
# =====================================================

print("\n====================================")
print("MONTHLY TRIP TRENDS")
print("====================================")

monthly_trips = (
    cleaned_df
    .withColumn(
        "trip_year",
        year("tpep_pickup_datetime")
    )
    .withColumn(
        "trip_month",
        month("tpep_pickup_datetime")
    )
    .groupBy("trip_year", "trip_month")
    .agg(count("*").alias("total_trips"))
    .orderBy("trip_year", "trip_month")
)

monthly_trips.show(100, truncate=False)

# =====================================================
# PEAK PICKUP HOURS
# =====================================================

print("\n====================================")
print("PEAK PICKUP HOURS")
print("====================================")

peak_hours = (
    cleaned_df
    .withColumn(
        "pickup_hour",
        hour("tpep_pickup_datetime")
    )
    .groupBy("pickup_hour")
    .agg(count("*").alias("total_trips"))
    .orderBy("pickup_hour")
)

peak_hours.show(24, truncate=False)

print("\nEDA COMPLETED SUCCESSFULLY.")

spark.stop()