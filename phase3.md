# NYC Taxi Big Data Analytics Pipeline

## Phase 3: Outlier Detection & Data Quality Assessment Report

### Objective

The objective of this phase was to identify abnormal, corrupted, and suspicious records within the NYC Yellow Taxi dataset before performing final data cleaning and business analytics.

The dataset spans January 2021 through April 2026 and contains over 213 million taxi trip records distributed across 64 Parquet files.

---

## Data Preparation

Before performing outlier analysis, the following validation rules were applied:

### Cleaning Rules

* Removed records with passenger_count <= 0
* Retained trips occurring only between 2021 and 2026
* Standardized timestamp fields
* Unified schema across all Parquet files

### Dataset Size

| Stage           |     Records |
| --------------- | ----------: |
| Raw Dataset     | 213,671,400 |
| Cleaned Dataset | 187,189,990 |

A total of 26.48 million records were removed during initial quality filtering.

---

## Percentile Analysis

To understand the distribution of key numerical variables, the 99th and 99.9th percentiles were calculated using Spark's approxQuantile() method.

### Fare Amount

| Metric            |      Value |
| ----------------- | ---------: |
| 99th Percentile   |      73.00 |
| 99.9th Percentile | 863,372.12 |

### Total Amount

| Metric            |      Value |
| ----------------- | ---------: |
| 99th Percentile   |     102.25 |
| 99.9th Percentile | 863,380.37 |

### Trip Distance

| Metric            |      Value |
| ----------------- | ---------: |
| 99th Percentile   |      20.05 |
| 99.9th Percentile | 186,967.57 |

### Tip Amount

| Metric            |    Value |
| ----------------- | -------: |
| 99th Percentile   |    17.19 |
| 99.9th Percentile | 1,400.16 |

---

## Key Findings

The 99th percentile values appear realistic and align with expected NYC taxi operations.

However, the 99.9th percentile values reveal significant data corruption.

### Finding 1: Corrupted Fare Records

Several trips contain fare amounts exceeding hundreds of thousands of dollars despite extremely short trip distances.

Examples:

| Distance (Miles) | Fare Amount ($) |
| ---------------- | --------------: |
| 1.6              |      863,372.12 |
| 2.5              |      818,283.44 |
| 3.3              |      401,092.32 |
| 1.2              |      395,844.94 |

These records are operationally impossible and indicate corrupted monetary fields.

---

### Finding 2: Corrupted Distance Records

Several records report distances comparable to interplanetary travel while charging standard taxi fares.

Examples:

| Distance (Miles) | Fare Amount ($) |
| ---------------- | --------------: |
| 186,967.57       |           11.68 |
| 184,340.80       |           38.08 |
| 164,072.79       |           16.00 |
| 161,726.10       |            8.00 |

Such values are physically impossible and indicate corruption within the trip_distance field.

---

### Finding 3: Extreme Tip Amounts

Several trips contained unusually large gratuities.

Examples:

| Fare ($) |  Tip ($) |
| -------- | -------: |
| 47.00    | 1,400.16 |
| 13.00    | 1,393.86 |
| 12.00    | 1,393.56 |
| 17.00    |   999.99 |

Although some large tips may be legitimate, these values were flagged for further investigation.

---

## Invalid Trip Detection

A dedicated validation framework was created to identify records violating basic business rules.

### Validation Rules

A trip was classified as invalid if:

* fare_amount < 0
* total_amount < 0
* trip_distance < 0
* trip_distance = 0 AND total_amount > 100
* fare_amount = 0 AND total_amount > 100

### Results

| Metric        |     Count |
| ------------- | --------: |
| Invalid Trips | 2,452,917 |

Examples include:

| Distance |   Fare |  Total |
| -------- | -----: | -----: |
| 12.95    | -41.50 | -45.30 |
| 5.31     | -16.00 | -19.80 |
| 0.28     |  -4.00 |  -7.80 |

These records were classified as corrupted transactions.

---

## Suspicious Trip Detection

Records were classified as suspicious if they met any of the following criteria:

* Total amount exceeds the 99.9th percentile
* Trip distance exceeds the 99.9th percentile
* Tip amount exceeds 5× fare amount

Invalid records were excluded from this category.

### Results

| Metric           |  Count |
| ---------------- | -----: |
| Suspicious Trips | 30,319 |

Examples include:

| Distance |  Fare |    Tip |
| -------- | ----: | -----: |
| 0.48     | 10.70 |  99.99 |
| 0.67     |  6.50 |  81.00 |
| 9.83     | 39.40 | 261.00 |
| 1.11     |  9.30 |  77.00 |

These records may represent:

* Data entry errors
* Fraudulent transactions
* Exceptional customer behavior
* Payment processing anomalies

---

## Overall Impact

| Category         |     Records |
| ---------------- | ----------: |
| Raw Trips        | 213,671,400 |
| Cleaned Trips    | 187,189,990 |
| Invalid Trips    |   2,452,917 |
| Suspicious Trips |      30,319 |

---

## Conclusion

The outlier analysis successfully identified large-scale data quality issues within the NYC Taxi dataset.

Major anomalies were discovered in monetary and distance-related attributes, including:

* Trips exceeding $863,000 in fare value
* Trips exceeding 186,000 miles in reported distance
* Over 2.45 million invalid transactions
* More than 30,000 suspicious transactions

These findings establish the foundation for the next phase of the project, where domain-specific cleaning rules will be developed to remove corrupted records while preserving legitimate extreme trips.

The resulting dataset will serve as the trusted source for revenue analytics, demand forecasting, anomaly detection, and business intelligence reporting.
