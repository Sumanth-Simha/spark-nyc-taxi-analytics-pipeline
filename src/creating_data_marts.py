from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("Create All Data Marts")
    .config("spark.driver.memory", "8g")
    .config("spark.executor.memory", "8g")
    .config("spark.sql.shuffle.partitions", "8")
    .enableHiveSupport()
    .getOrCreate()
)

spark.sql("USE nyc_taxi_dw")

print("=" * 60)
print("CREATING DATA MARTS")
print("=" * 60)

# ==========================================================
# 1. YEARLY REVENUE MART
# ==========================================================

print("\nCreating mart_yearly_revenue...")

spark.sql("""
DROP TABLE IF EXISTS mart_yearly_revenue
""")

spark.sql("""
CREATE TABLE mart_yearly_revenue AS
SELECT
    YEAR(tpep_pickup_datetime) AS year,
    COUNT(*) AS total_trips,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_trip_revenue,
    ROUND(AVG(trip_distance), 2) AS avg_trip_distance
FROM fact_taxi_trips
GROUP BY YEAR(tpep_pickup_datetime)
""")

# ==========================================================
# 2. PEAK HOURS MART
# ==========================================================

print("Creating mart_peak_hours...")

spark.sql("""
DROP TABLE IF EXISTS mart_peak_hours
""")

spark.sql("""
CREATE TABLE mart_peak_hours AS
SELECT
    HOUR(tpep_pickup_datetime) AS pickup_hour,
    COUNT(*) AS total_trips,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_fare
FROM fact_taxi_trips
GROUP BY HOUR(tpep_pickup_datetime)
""")

# ==========================================================
# 3. PAYMENT ANALYTICS MART
# ==========================================================

print("Creating mart_payment_analysis...")

spark.sql("""
DROP TABLE IF EXISTS mart_payment_analysis
""")

spark.sql("""
CREATE TABLE mart_payment_analysis AS
SELECT
    payment_type,
    COUNT(*) AS total_trips,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(tip_amount), 2) AS avg_tip,
    ROUND(SUM(tip_amount), 2) AS total_tip_amount
FROM fact_taxi_trips
GROUP BY payment_type
""")

# ==========================================================
# 4. LOCATION ANALYTICS MART
# ==========================================================

print("Creating mart_location_analysis...")

spark.sql("""
DROP TABLE IF EXISTS mart_location_analysis
""")

spark.sql("""
CREATE TABLE mart_location_analysis AS
SELECT
    PULocationID,
    COUNT(*) AS total_trips,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_fare,
    ROUND(AVG(tip_amount), 2) AS avg_tip
FROM fact_taxi_trips
GROUP BY PULocationID
""")

# ==========================================================
# 5. DISTANCE ANALYTICS MART
# ==========================================================

print("Creating mart_distance_analysis...")

spark.sql("""
DROP TABLE IF EXISTS mart_distance_analysis
""")

spark.sql("""
CREATE TABLE mart_distance_analysis AS
SELECT
    CASE
        WHEN trip_distance < 2 THEN 'Short (<2 Miles)'
        WHEN trip_distance BETWEEN 2 AND 5 THEN 'Medium (2-5 Miles)'
        WHEN trip_distance BETWEEN 5 AND 10 THEN 'Long (5-10 Miles)'
        ELSE 'Very Long (>10 Miles)'
    END AS distance_category,

    COUNT(*) AS total_trips,
    ROUND(AVG(total_amount), 2) AS avg_revenue,
    ROUND(SUM(total_amount), 2) AS total_revenue

FROM fact_taxi_trips
GROUP BY
    CASE
        WHEN trip_distance < 2 THEN 'Short (<2 Miles)'
        WHEN trip_distance BETWEEN 2 AND 5 THEN 'Medium (2-5 Miles)'
        WHEN trip_distance BETWEEN 5 AND 10 THEN 'Long (5-10 Miles)'
        ELSE 'Very Long (>10 Miles)'
    END
""")

# ==========================================================
# SHOW CREATED MARTS
# ==========================================================

print("\n")
print("=" * 60)
print("AVAILABLE TABLES")
print("=" * 60)

spark.sql("""
SHOW TABLES
""").show(truncate=False)

print("\n")
print("=" * 60)
print("YEARLY REVENUE MART SAMPLE")
print("=" * 60)

spark.sql("""
SELECT *
FROM mart_yearly_revenue
ORDER BY year
""").show()

print("\nAll Data Marts Created Successfully!")



# ==========================================================
# EXPORT ALL MARTS AS CSV
# ==========================================================

print("\nExporting marts to CSV files...")

marts = [
    "mart_yearly_revenue",
    "mart_peak_hours",
    "mart_payment_analysis",
    "mart_location_analysis",
    "mart_distance_analysis"
]

for mart in marts:
    print(f"Exporting {mart}...")

    df = spark.sql(f"SELECT * FROM {mart}")

    (
        df.coalesce(1)    # creates a single CSV file
          .write
          .mode("overwrite")
          .option("header", "true")
          .csv(f"artifacts/data_marts/{mart}")
    )

print("All marts exported successfully!")

spark.stop()