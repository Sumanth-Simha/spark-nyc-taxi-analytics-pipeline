## Phase 7 - Hive Data Warehouse

### Objective

Build a Hive-based data warehouse layer on top of the cleaned NYC Taxi dataset.

### Activities

* Installed and configured Apache Hive.
* Enabled Hive support in Spark.
* Created Hive database `nyc_taxi_dw`.
* Registered cleaned parquet dataset (`clean_category_C`) as an external Hive table.
* Verified successful integration between Spark SQL and Hive Metastore.

### Challenges Encountered

* Hive environment variable configuration issues.
* Incorrect table location registration resulting in zero-row tables.
* Failed managed-table approach due to Java heap space limitations.
* Accidental overwrite attempt on the final dataset, requiring recovery from the preserved `clean_category_C` dataset.

### Final Outcome

* Hive external table `fact_taxi_trips` successfully created.
* Verified row count: **186,394,753 records**.
* Warehouse layer ready for creation of analytical data marts and business intelligence queries.
