from pyspark.sql import SparkSession
from pyspark.sql.functions import col, unix_timestamp

# ==========================================================
# SPARK SESSION
# ==========================================================

spark = (
    SparkSession.builder
    .appName("NYC Taxi - Category C Cleaning")
    .config("spark.driver.memory", "4g")
    .config("spark.executor.memory", "4g")
    .config("spark.sql.shuffle.partitions", "8")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

print("Spark Session Created")

# ==========================================================
# LOAD CATEGORY B OUTPUT
# ==========================================================

INPUT_PATH = "artifacts/clean_category_B"

df = spark.read.parquet(INPUT_PATH)

before_count = df.count()

print("\nDataset Loaded Successfully")
print(f"Records Before Cleaning: {before_count:,}")

# ==========================================================
# CREATE DURATION COLUMN
# ==========================================================

df = df.withColumn(
    "duration_minutes",
    (
        unix_timestamp("tpep_dropoff_datetime")
        - unix_timestamp("tpep_pickup_datetime")
    ) / 60.0
)

# ==========================================================
# CATEGORY C RULE 1
# REMOVE INVALID DURATIONS
# ==========================================================

invalid_duration = df.filter(
    col("duration_minutes") <= 0
)

invalid_duration_count = invalid_duration.count()

# Save removed records

invalid_duration.write.mode("overwrite").parquet(
    "artifacts/category_C_removed_invalid_duration"
)

# Keep valid records

df = df.filter(
    col("duration_minutes") > 0
)

# ==========================================================
# CATEGORY C RULE 2
# PASSENGER COUNT <= 8
# ==========================================================

invalid_passenger = df.filter(
    col("passenger_count") > 8
)

invalid_passenger_count = invalid_passenger.count()

# Save removed records

invalid_passenger.write.mode("overwrite").parquet(
    "artifacts/category_C_removed_passenger"
)

# Keep valid records

df = df.filter(
    col("passenger_count") <= 8
)

# ==========================================================
# FINAL COUNT
# ==========================================================

after_count = df.count()

total_removed = before_count - after_count

# ==========================================================
# SAVE CLEAN DATASET
# ==========================================================

OUTPUT_PATH = "artifacts/clean_category_C"

df.write.mode("overwrite").parquet(OUTPUT_PATH)

# ==========================================================
# REPORT
# ==========================================================

REPORT_PATH = "artifacts/category_C_cleaning_report.txt"

with open(REPORT_PATH, "w") as f:

    f.write("CATEGORY C CLEANING REPORT\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Records Before Cleaning : {before_count:,}\n")
    f.write(f"Records After Cleaning  : {after_count:,}\n")
    f.write(f"Total Removed           : {total_removed:,}\n\n")

    f.write("BREAKDOWN\n")
    f.write("-" * 60 + "\n")

    f.write(
        f"Duration <= 0 mins      : "
        f"{invalid_duration_count:,}\n"
    )

    f.write(
        f"Passenger Count > 8     : "
        f"{invalid_passenger_count:,}\n"
    )

print("\n" + "=" * 60)
print("CATEGORY C CLEANING SUMMARY")
print("=" * 60)

print(f"Records Before Cleaning : {before_count:,}")
print(f"Records After Cleaning  : {after_count:,}")
print(f"Total Removed           : {total_removed:,}")

print("\nBreakdown")

print(
    f"Duration <= 0 mins      : "
    f"{invalid_duration_count:,}"
)

print(
    f"Passenger Count > 8     : "
    f"{invalid_passenger_count:,}"
)

print("\nOutputs Saved")

print("artifacts/clean_category_C")
print("artifacts/category_C_removed_invalid_duration")
print("artifacts/category_C_removed_passenger")
print("artifacts/category_C_cleaning_report.txt")

spark.stop()

print("\nCATEGORY C CLEANING COMPLETE")