from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    unix_timestamp,
    count,
    try_divide,
    round
)

# ==========================================================
# SPARK SESSION
# ==========================================================

spark = (
    SparkSession.builder
    .appName("NYC Taxi - Category C Investigation")
    .config("spark.driver.memory", "4g")
    .config("spark.executor.memory", "4g")
    .config("spark.sql.shuffle.partitions", "8")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

print("Spark Session Created")

# ==========================================================
# LOAD DATA
# ==========================================================

INPUT_PATH = "artifacts/clean_category_B"

df = spark.read.parquet(INPUT_PATH)

total_records = df.count()

print("\nDataset Loaded Successfully")
print(f"Records Loaded: {total_records:,}")

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
# CATEGORY C1 - DURATION
# ==========================================================

print("\n" + "=" * 60)
print("CATEGORY C1 - DURATION ANALYSIS")
print("=" * 60)

invalid_duration = df.filter(
    col("duration_minutes") <= 0
)

duration_gt_24h = df.filter(
    col("duration_minutes") > 1440
)

duration_gt_48h = df.filter(
    col("duration_minutes") > 2880
)

invalid_duration_count = invalid_duration.count()
duration_24_count = duration_gt_24h.count()
duration_48_count = duration_gt_48h.count()

print(f"Duration <= 0 mins : {invalid_duration_count:,}")
print(f"Duration > 24 hrs  : {duration_24_count:,}")
print(f"Duration > 48 hrs  : {duration_48_count:,}")

# Save evidence
invalid_duration.write.mode("overwrite").parquet(
    "artifacts/category_C_invalid_duration"
)

# ==========================================================
# CATEGORY C2 - SPEED
# ==========================================================

print("\n" + "=" * 60)
print("CATEGORY C2 - SPEED ANALYSIS")
print("=" * 60)

speed_df = (
    df
    .filter(col("duration_minutes") > 0)
    .withColumn(
        "duration_hours",
        col("duration_minutes") / 60.0
    )
)

speed_df = speed_df.withColumn(
    "speed_mph",
    round(
        try_divide(
            col("trip_distance"),
            col("duration_hours")
        ),
        2
    )
)

speed_df = speed_df.filter(
    col("speed_mph").isNotNull()
)

speed_80_count = speed_df.filter(
    col("speed_mph") > 80
).count()

speed_100_count = speed_df.filter(
    col("speed_mph") > 100
).count()

speed_120_count = speed_df.filter(
    col("speed_mph") > 120
).count()

speed_150_count = speed_df.filter(
    col("speed_mph") > 150
).count()

print(f"Speed > 80 mph  : {speed_80_count:,}")
print(f"Speed > 100 mph : {speed_100_count:,}")
print(f"Speed > 120 mph : {speed_120_count:,}")
print(f"Speed > 150 mph : {speed_150_count:,}")

speed_df.filter(
    col("speed_mph") > 150
).write.mode("overwrite").parquet(
    "artifacts/category_C_speed_gt_150"
)

# ==========================================================
# CATEGORY C3 - DISTANCE VS FARE
# ==========================================================

print("\n" + "=" * 60)
print("CATEGORY C3 - DISTANCE / FARE ANALYSIS")
print("=" * 60)

distance_zero_fare_positive = df.filter(
    (col("trip_distance") == 0)
    & (col("fare_amount") > 0)
)

distance_positive_fare_zero = df.filter(
    (col("trip_distance") > 0)
    & (col("fare_amount") == 0)
)

distance_zero_count = distance_zero_fare_positive.count()
fare_zero_count = distance_positive_fare_zero.count()

print(f"Distance=0 & Fare>0 : {distance_zero_count:,}")
print(f"Distance>0 & Fare=0 : {fare_zero_count:,}")

distance_zero_fare_positive.write.mode(
    "overwrite"
).parquet(
    "artifacts/category_C_distance0_fare_positive"
)

distance_positive_fare_zero.write.mode(
    "overwrite"
).parquet(
    "artifacts/category_C_distance_positive_fare0"
)

# ==========================================================
# CATEGORY C4 - PASSENGERS
# ==========================================================

print("\n" + "=" * 60)
print("CATEGORY C4 - PASSENGER ANALYSIS")
print("=" * 60)

(
    df.groupBy("passenger_count")
    .agg(count("*").alias("records"))
    .orderBy("passenger_count")
    .show(50, False)
)

passenger_gt_8_count = df.filter(
    col("passenger_count") > 8
).count()

print(f"Passenger Count > 8 : {passenger_gt_8_count:,}")

# ==========================================================
# CATEGORY C5 - TIP ANALYSIS
# ==========================================================

print("\n" + "=" * 60)
print("CATEGORY C5 - TIP ANALYSIS")
print("=" * 60)

tip_gt_fare_count = df.filter(
    col("tip_amount") > col("fare_amount")
).count()

tip_gt_2x_count = df.filter(
    col("tip_amount") > col("fare_amount") * 2
).count()

tip_gt_5x_count = df.filter(
    col("tip_amount") > col("fare_amount") * 5
).count()

print(f"Tip > Fare     : {tip_gt_fare_count:,}")
print(f"Tip > 2x Fare  : {tip_gt_2x_count:,}")
print(f"Tip > 5x Fare  : {tip_gt_5x_count:,}")

# ==========================================================
# REPORT
# ==========================================================

report_path = "artifacts/category_C_report.txt"

with open(report_path, "w") as f:

    f.write("CATEGORY C INVESTIGATION REPORT\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Total Records: {total_records:,}\n\n")

    f.write("DURATION ANALYSIS\n")
    f.write(f"Duration <= 0 : {invalid_duration_count:,}\n")
    f.write(f"Duration >24h : {duration_24_count:,}\n")
    f.write(f"Duration >48h : {duration_48_count:,}\n\n")

    f.write("SPEED ANALYSIS\n")
    f.write(f"Speed >80mph  : {speed_80_count:,}\n")
    f.write(f"Speed >100mph : {speed_100_count:,}\n")
    f.write(f"Speed >120mph : {speed_120_count:,}\n")
    f.write(f"Speed >150mph : {speed_150_count:,}\n\n")

    f.write("DISTANCE / FARE\n")
    f.write(f"Distance=0 Fare>0 : {distance_zero_count:,}\n")
    f.write(f"Distance>0 Fare=0 : {fare_zero_count:,}\n\n")

    f.write("PASSENGERS\n")
    f.write(f"Passenger > 8 : {passenger_gt_8_count:,}\n\n")

    f.write("TIP ANALYSIS\n")
    f.write(f"Tip > Fare : {tip_gt_fare_count:,}\n")
    f.write(f"Tip >2x    : {tip_gt_2x_count:,}\n")
    f.write(f"Tip >5x    : {tip_gt_5x_count:,}\n")

print("\nReport Saved")
print(report_path)

spark.stop()

print("\nCATEGORY C INVESTIGATION COMPLETE")