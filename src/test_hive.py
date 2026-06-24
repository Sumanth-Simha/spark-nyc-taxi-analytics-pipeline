from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("Hive Test")
    .enableHiveSupport()
    .getOrCreate()
)

print("Spark Started")

spark.sql("CREATE DATABASE IF NOT EXISTS test_db")

print("Database Created")

spark.sql("SHOW DATABASES").show(truncate=False)

spark.stop()