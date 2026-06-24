from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .enableHiveSupport()
    .getOrCreate()
)

spark.sql("USE nyc_taxi_dw")

spark.sql("""
DESCRIBE EXTENDED fact_taxi_trips
""").show(200, False)

spark.stop()