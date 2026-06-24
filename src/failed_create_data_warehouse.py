from pyspark.sql import SparkSession

# Create Spark Session with Hive Support
spark = (
    SparkSession.builder
    .appName("NYC Taxi Data Warehouse")
    .enableHiveSupport()
    .getOrCreate()
)

# Create Database
spark.sql("""
CREATE DATABASE IF NOT EXISTS nyc_taxi_dw
""")

spark.sql("USE nyc_taxi_dw")

# Load Final Dataset
df = spark.read.parquet("artifacts/final_dataset")

print(f"Rows Loaded: {df.count():,}")

# Create Main Fact Table
df.write \
    .mode("overwrite") \
    .format("parquet") \
    .saveAsTable("fact_taxi_trips")

print("Fact Table Created")

# Verify
spark.sql("SHOW TABLES").show(truncate=False)

spark.stop()