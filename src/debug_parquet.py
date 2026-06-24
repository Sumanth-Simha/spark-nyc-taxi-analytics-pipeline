from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("DebugDW")
    .enableHiveSupport()
    .getOrCreate()
)

df = spark.read.parquet("artifacts/final_dataset")

print("PARQUET COUNT:")
print(df.count())

df.printSchema()

df.show(5)

spark.stop()