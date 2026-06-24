from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

df = spark.read.parquet("artifacts/final_dataset")

df.printSchema()

print("Rows:", df.count())

spark.stop()