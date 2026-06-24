# src/recreate_final_dataset.py

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("Recreate Final Dataset")
    .getOrCreate()
)

df = spark.read.parquet("artifacts/clean_category_C")

print("Input Rows:", df.count())

df.write.mode("overwrite").parquet(
    "artifacts/final_dataset"
)

print("Final Dataset Recreated")

spark.stop()