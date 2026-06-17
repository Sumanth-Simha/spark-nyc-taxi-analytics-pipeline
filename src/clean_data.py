from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("NYC Taxi Data Cleaning") \
    .getOrCreate()

# Load raw data
df = spark.read.parquet("data/*.parquet")

print("Raw Records:", df.count())

print("\nNegative or Zero Distances:")
print(df.filter(col("trip_distance") <= 0).count())

print("\nNegative or Zero Fare:")
print(df.filter(col("fare_amount") <= 0).count())

print("\nNegative Passenger Count:")
print(df.filter(col("passenger_count") <= 0).count())

print("\nNull Pickup Time:")
print(df.filter(col("tpep_pickup_datetime").isNull()).count())

print("\nNull Dropoff Time:")
print(df.filter(col("tpep_dropoff_datetime").isNull()).count())