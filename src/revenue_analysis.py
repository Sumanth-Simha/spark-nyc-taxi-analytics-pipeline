from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, year, sum, avg, max, round
)
from functools import reduce
import glob

# -------------------------
# Create Spark Session
# -------------------------
spark = (
    SparkSession.builder
    .appName("NYC Taxi Revenue Analysis")
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
# Cleaning
# -------------------------
cleaned_df = (
    df
    .filter(col("passenger_count") > 0)
    .filter(year("tpep_pickup_datetime").between(2021, 2026))
)

# -------------------------
# Overall Revenue Metrics
# -------------------------
print("\n====================================")
print("OVERALL REVENUE METRICS")
print("====================================")

overall = cleaned_df.select(
    round(sum("total_amount"), 2).alias("Total Revenue ($)"),
    round(avg("fare_amount"), 2).alias("Average Fare ($)"),
    round(avg("tip_amount"), 2).alias("Average Tip ($)"),
    round(max("total_amount"), 2).alias("Highest Trip Amount ($)")
)

overall.show(truncate=False)

# -------------------------
# Revenue by Year
# -------------------------
print("\n====================================")
print("REVENUE BY YEAR")
print("====================================")

yearly_revenue = (
    cleaned_df
    .withColumn(
        "trip_year",
        year("tpep_pickup_datetime")
    )
    .groupBy("trip_year")
    .agg(
        round(sum("total_amount"), 2).alias("Revenue ($)")
    )
    .orderBy("trip_year")
)

yearly_revenue.show(truncate=False)

print("\nREVENUE ANALYSIS COMPLETED.")
print("\n====================================")
print("TOP 10 MOST EXPENSIVE TRIPS")
print("====================================")

cleaned_df.select(
    "tpep_pickup_datetime",
    "trip_distance",
    "fare_amount",
    "tip_amount",
    "total_amount",
    "PULocationID",
    "DOLocationID"
).orderBy(
    col("total_amount").desc()
).show(10, truncate=False)



print("\n====================================")
print("FARE OUTLIERS")
print("====================================")

print(
    "Trips with total_amount > $1000:",
    cleaned_df.filter(col("total_amount") > 1000).count()
)

print(
    "Trips with fare_amount > $1000:",
    cleaned_df.filter(col("fare_amount") > 1000).count()
)

spark.stop()