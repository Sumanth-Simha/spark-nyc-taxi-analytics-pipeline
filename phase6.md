# Phase 6: Hive Environment Setup & Artifact Consolidation

## Objective

After completing data cleaning, anomaly detection, and validation workflows, the project contained multiple intermediate datasets generated during exploratory analysis and iterative cleaning operations.

The objective of this phase was to:

* Configure Apache Hive for data warehousing.
* Prepare the project for Hive integration.
* Remove redundant intermediate datasets.
* Retain only production-ready datasets and audit artifacts.

---

## Hive Setup

Apache Hive was installed and configured successfully.

Key components initialized:

* Hive Metastore
* Embedded Derby Database
* Warehouse Directory
* Hive CLI Environment

Verification steps included:

* Launching Hive shell
* Creating and accessing databases
* Confirming metastore initialization
* Verifying Spark-Hive compatibility

Generated Hive artifacts:

```text
metastore_db/
derby.log
```

These files confirm successful Hive metastore initialization.

---

## Artifact Review

During previous cleaning phases, multiple intermediate datasets were generated for investigation and validation purposes.

### Removed Artifacts

The following datasets were identified as temporary processing outputs and removed:

```text
category_B
category_B_removed

clean_category_A
clean_category_B

category_C_distance0_fare_positive
category_C_distance_positive_fare0

category_C_invalid_duration
category_C_removed_invalid_duration

category_C_removed_passenger

category_C_speed_gt_150
```

These datasets had already served their purpose during quality assessment and cleaning validation.

---

## Spark Temporary Data Cleanup

Several Spark-generated temporary directories were also removed:

```text
spark-*
```

These folders contained temporary execution data and were not required for future analysis.

---

## Retained Artifacts

The following datasets were preserved:

```text
artifacts/
├── clean_category_C
├── invalid_trips
├── suspicious_trips
├── category_C_report.txt
└── category_C_cleaning_report.txt
```

### Purpose

#### clean_category_C

Final production-ready dataset after all cleaning operations.

#### invalid_trips

Contains records removed due to data quality violations.

#### suspicious_trips

Contains anomalous transactions identified during outlier analysis.

#### category_C_report.txt

Summary of Category C anomaly investigations.

#### category_C_cleaning_report.txt

Detailed record of cleaning decisions and removed records.

---

## Outcome

The project structure was streamlined and prepared for warehouse integration.

Benefits achieved:

* Reduced storage consumption
* Eliminated redundant datasets
* Improved project maintainability
* Simplified repository structure
* Prepared final dataset for Hive warehousing

---

## Next Phase

Phase 7 will focus on Hive-based data warehousing, including:

* Database creation
* External table creation
* HiveQL analytics
* Summary table generation
* Business intelligence reporting
