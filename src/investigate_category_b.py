from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# =====================================================
# CREATE SPARK SESSION
# =====================================================

spark = (
    SparkSession.builder
    .appName("NYC Taxi Category B Investigation")
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

clean_df = spark.read.parquet(
    "artifacts/clean_category_A"
)

print("\nDataset Loaded Successfully")

print(
    f"Records Available: "
    f"{clean_df.count():,}"
)

# =====================================================
# EXTREME FARE INVESTIGATION
# =====================================================

print("\n======================================")
print("FARE > $10,000")
print("======================================")

extreme_fare = clean_df.filter(
    col("fare_amount") > 10000
)

print(
    f"Extreme Fare Records: "
    f"{extreme_fare.count():,}"
)

extreme_fare.select(
    "trip_distance",
    "fare_amount",
    "tip_amount",
    "total_amount"
).orderBy(
    col("fare_amount").desc()
).show(
    50,
    truncate=False
)

# =====================================================
# EXTREME TOTAL INVESTIGATION
# =====================================================

print("\n======================================")
print("TOTAL AMOUNT > $10,000")
print("======================================")

extreme_total = clean_df.filter(
    col("total_amount") > 10000
)

print(
    f"Extreme Total Records: "
    f"{extreme_total.count():,}"
)

extreme_total.select(
    "trip_distance",
    "fare_amount",
    "tip_amount",
    "total_amount"
).orderBy(
    col("total_amount").desc()
).show(
    50,
    truncate=False
)

# =====================================================
# EXTREME DISTANCE INVESTIGATION
# =====================================================

print("\n======================================")
print("DISTANCE > 1,000 MILES")
print("======================================")

extreme_distance = clean_df.filter(
    col("trip_distance") > 1000
)

print(
    f"Extreme Distance Records: "
    f"{extreme_distance.count():,}"
)

extreme_distance.select(
    "trip_distance",
    "fare_amount",
    "tip_amount",
    "total_amount"
).orderBy(
    col("trip_distance").desc()
).show(
    100,
    truncate=False
)

# =====================================================
# EXTREME TIP INVESTIGATION
# =====================================================

print("\n======================================")
print("TIP > $1,000")
print("======================================")

extreme_tip = clean_df.filter(
    col("tip_amount") > 1000
)

print(
    f"Extreme Tip Records: "
    f"{extreme_tip.count():,}"
)

extreme_tip.select(
    "trip_distance",
    "fare_amount",
    "tip_amount",
    "total_amount"
).orderBy(
    col("tip_amount").desc()
).show(
    50,
    truncate=False
)

# =====================================================
# SAVE INVESTIGATION DATASETS
# =====================================================

extreme_fare.write.mode("overwrite").parquet(
    "artifacts/category_B/extreme_fare"
)

extreme_total.write.mode("overwrite").parquet(
    "artifacts/category_B/extreme_total"
)

extreme_distance.write.mode("overwrite").parquet(
    "artifacts/category_B/extreme_distance"
)

extreme_tip.write.mode("overwrite").parquet(
    "artifacts/category_B/extreme_tip"
)

print("\n======================================")
print("FILES SAVED")
print("======================================")

print("artifacts/category_B/extreme_fare")
print("artifacts/category_B/extreme_total")
print("artifacts/category_B/extreme_distance")
print("artifacts/category_B/extreme_tip")

# =====================================================
# SUMMARY
# =====================================================

print("\n======================================")
print("CATEGORY B SUMMARY")
print("======================================")

print(
    f"Fare > 10,000      : "
    f"{extreme_fare.count():,}"
)

print(
    f"Total > 10,000     : "
    f"{extreme_total.count():,}"
)

print(
    f"Distance > 1,000   : "
    f"{extreme_distance.count():,}"
)

print(
    f"Tip > 1,000        : "
    f"{extreme_tip.count():,}"
)

print("\nCategory B Investigation Complete.")

spark.stop()