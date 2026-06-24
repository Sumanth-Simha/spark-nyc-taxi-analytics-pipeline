from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("Data Marts")
    .enableHiveSupport()
    .getOrCreate()
)

spark.sql("USE nyc_taxi_dw")

spark.sql("""
DROP TABLE IF EXISTS mart_yearly_revenue
""")

spark.sql("""
CREATE TABLE mart_yearly_revenue AS
SELECT
    YEAR(tpep_pickup_datetime) AS year,
    COUNT(*) AS trips,
    ROUND(SUM(total_amount),2) AS revenue
FROM fact_taxi_trips
GROUP BY YEAR(tpep_pickup_datetime)
""")

df = spark.sql("""
SELECT *
FROM mart_yearly_revenue
ORDER BY year
""")

df.toPandas().to_csv(
    "artifacts/mart_yearly_revenue.csv",
    index=False
)
spark.sql("""
DESCRIBE EXTENDED mart_yearly_revenue
""").show(200, False)
spark.stop()