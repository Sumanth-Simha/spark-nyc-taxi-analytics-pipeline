from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# =====================================================
# CREATE SPARK SESSION
# =====================================================

spark = (
    SparkSession.builder
    .appName("NYC Taxi Category B Cleaning")
    .config("spark.driver.memory", "4g")
    .config("spark.executor.memory", "4g")
    .config("spark.sql.shuffle.partitions", "8")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

print("\nSpark Session Created")

# =====================================================
# LOAD CATEGORY A CLEAN DATASET
# =====================================================

df = spark.read.parquet(
    "artifacts/clean_category_A"
)

print("\nDataset Loaded Successfully")

# =====================================================
# RECORDS BEFORE CLEANING
# =====================================================

before_count = df.count()

print(f"\nRecords Before Cleaning: {before_count:,}")

# =====================================================
# COUNT CATEGORY B RECORDS
# =====================================================

fare_over_10000 = df.filter(
    col("fare_amount") > 10000
)

total_over_10000 = df.filter(
    col("total_amount") > 10000
)

distance_over_1000 = df.filter(
    col("trip_distance") > 1000
)

fare_count = fare_over_10000.count()
total_count = total_over_10000.count()
distance_count = distance_over_1000.count()

# =====================================================
# CATEGORY B CLEANING
# =====================================================

clean_df = df.filter(
    (col("fare_amount") <= 10000)
    &
    (col("total_amount") <= 10000)
    &
    (col("trip_distance") <= 1000)
)

# =====================================================
# RECORDS AFTER CLEANING
# =====================================================

after_count = clean_df.count()

removed_count = before_count - after_count

# =====================================================
# SAVE CLEAN DATASET
# =====================================================

clean_df.write.mode("overwrite").parquet(
    "artifacts/clean_category_B"
)

# =====================================================
# SAVE REMOVED RECORDS
# =====================================================

removed_df = df.subtract(clean_df)

removed_df.write.mode("overwrite").parquet(
    "artifacts/category_B_removed"
)

# =====================================================
# SUMMARY
# =====================================================

print("\n======================================")
print("CATEGORY B CLEANING SUMMARY")
print("======================================")

print(
    f"Records Before Cleaning : {before_count:,}"
)

print(
    f"Records After Cleaning  : {after_count:,}"
)

print(
    f"Total Removed           : {removed_count:,}"
)

print("\nBreakdown")

print(
    f"Fare > 10,000      : {fare_count:,}"
)

print(
    f"Total > 10,000     : {total_count:,}"
)

print(
    f"Distance > 1,000   : {distance_count:,}"
)

print("\nOutputs Saved")

print(
    "artifacts/clean_category_B"
)

print(
    "artifacts/category_B_removed"
)

spark.stop()