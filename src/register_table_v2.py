from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("Register Table V2")
    .enableHiveSupport()
    .getOrCreate()
)

spark.sql("CREATE DATABASE IF NOT EXISTS nyc_taxi_dw")
spark.sql("USE nyc_taxi_dw")

# Remove old broken table
spark.sql("DROP TABLE IF EXISTS fact_taxi_trips")

# Read actual parquet
df = spark.read.parquet("artifacts/final_dataset")

# Register as external table
(
    df.write
      .mode("overwrite")
      .option(
          "path",
          r"C:\Users\rsuma\OneDrive\Desktop\My Project\NYC_taxi\artifacts\final_dataset"
      )
      .saveAsTable("fact_taxi_trips")
)

print("Table Registered")

spark.sql("SHOW TABLES").show(truncate=False)

spark.stop()