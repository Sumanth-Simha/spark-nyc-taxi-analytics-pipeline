from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("Register Hive Table")
    .enableHiveSupport()
    .getOrCreate()
)

spark.sql("CREATE DATABASE IF NOT EXISTS nyc_taxi_dw")
spark.sql("USE nyc_taxi_dw")

spark.sql("DROP TABLE IF EXISTS fact_taxi_trips")

spark.sql("""
CREATE TABLE fact_taxi_trips
USING PARQUET
LOCATION 'file:///C:/Users/rsuma/OneDrive/Desktop/My Project/NYC_taxi/artifacts/clean_category_C'
""")

print("Table created")

spark.sql("SHOW TABLES").show(truncate=False)

spark.stop()