from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year
from functools import reduce
import glob
import os

# -------------------------
# Create Spark Session
# -------------------------
spark = (
    SparkSession.builder
    .appName("NYC Taxi Pipeline")
    .config("spark.driver.memory", "4g")
    .config("spark.executor.memory", "4g")
    .config("spark.sql.shuffle.partitions", "8")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

# Avoid parquet reader issues
spark.conf.set(
    "spark.sql.parquet.enableVectorizedReader",
    "false"
)

# -------------------------
# Read parquet files
# -------------------------
parquet_files = sorted(glob.glob("data/*.parquet"))

if not parquet_files:
    raise Exception("No parquet files found!")

print(f"\nFound {len(parquet_files)} parquet files.\n")

dfs = []

for file in parquet_files:
    print(f"Reading: {os.path.basename(file)}")

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

# -------------------------
# Combine datasets
# -------------------------
df = reduce(
    lambda df1, df2: df1.unionByName(
        df2,
        allowMissingColumns=True
    ),
    dfs
)

# -------------------------
# Raw Dataset Statistics
# -------------------------
raw_total = df.count()

print("\n==============================")
print("RAW DATASET")
print("==============================")
print(f"Raw Records: {raw_total:,}")

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

cleaned_total = cleaned_df.count()

print("\n==============================")
print("CLEANING")
print("==============================")
print(f"Cleaned Records: {cleaned_total:,}")
print(f"Removed Records: {raw_total - cleaned_total:,}")

# -------------------------
# Trips by Year
# -------------------------
print("\n==============================")
print("TRIPS BY YEAR")
print("==============================")

cleaned_df.withColumn(
    "trip_year",
    year("tpep_pickup_datetime")
).groupBy(
    "trip_year"
).count().orderBy(
    "trip_year"
).show(100, truncate=False)

# -------------------------
# Trips by Vendor
# -------------------------
print("\n==============================")
print("TRIPS BY VENDOR")
print("==============================")

cleaned_df.groupBy(
    "VendorID"
).count().show()

# -------------------------
# Trips by Payment Type
# -------------------------
print("\n==============================")
print("TRIPS BY PAYMENT TYPE")
print("==============================")

cleaned_df.groupBy(
    "payment_type"
).count().show()

print("\nPipeline completed successfully.")

spark.stop()