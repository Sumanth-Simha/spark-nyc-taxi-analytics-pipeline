from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .enableHiveSupport()
    .getOrCreate()
)

spark.sql("USE nyc_taxi_dw")

spark.sql("""
SELECT COUNT(*) AS total_records
FROM fact_taxi_trips
""").show()

spark.stop()