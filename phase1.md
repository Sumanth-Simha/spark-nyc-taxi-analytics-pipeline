# Data Quality Issues and Cleaning Notes

## NYC Yellow Taxi Big Data Project

### Dataset Overview

* Dataset: NYC Yellow Taxi Trip Records
* Period Covered: January 2021 – April 2026
* Number of Source Files: 64 Parquet files
* Initial Dataset Size: **213,671,400 records**

---

## 1. Missing Monthly Data Discovery

### Issue

During the initial loading phase, the number of processed records was lower than expected.

### Root Cause

One of the monthly files (`yellow_tripdata_2021-05.parquet`) was missing from the dataset folder.

### Resolution

The missing file was downloaded and added to the dataset.

### Impact

* Before Fix: 63 files processed
* After Fix: 64 files processed
* Dataset size increased to the expected volume.

---

## 2. Invalid Passenger Counts

### Issue

The `passenger_count` field contained invalid values.

### Findings

| Passenger Count |    Records |
| --------------- | ---------: |
| NULL            | 23,716,389 |
| 0               |  2,764,050 |

### Resolution

Records were filtered using:

```python
passenger_count > 0
```

### Impact

Records Removed:

26,480,439

---

## 3. Timestamp Anomalies

### Issue

Exploratory analysis revealed trips occurring outside the study period.

Examples included:

* 2001
* 2002
* 2003
* 2008
* 2070
* 2098

### Investigation

Initially, it was unclear whether the problem originated from:

* corrupted source records, or
* schema inconsistencies during dataset union.

Timestamp columns were standardized before analysis.

### Resolution

Trips were restricted to the intended study period:

```python
year(tpep_pickup_datetime).between(2021, 2026)
```

### Impact

Only a very small number of records were affected.

---

## 4. Extreme Revenue Outliers

### Issue

Revenue analysis identified unrealistic fare values.

Examples:

| Distance  | Total Amount |
| --------- | -----------: |
| 1.6 miles |  $863,380.37 |
| 2.5 miles |  $818,286.74 |
| 0.0 miles |  $398,469.20 |
| 5.7 miles |  $395,854.74 |

### Investigation

The trips had:

* extremely short distances,
* zero tips,
* implausibly high fares.

These were determined to be data entry errors or corrupted financial records.

### Findings

Trips with:

* `total_amount > $1000` : 256
* `fare_amount > $1000` : 209

Percentage of affected trips:

0.000137% of the cleaned dataset.

### Resolution

```python
total_amount > 0
total_amount <= 1000
```

### Impact

Records Removed:

256

---

## 5. Schema Standardization Challenges

### Issue

Parquet files from different years contained slight schema variations.

Observed differences included:

* `timestamp` vs `timestamp_ntz`
* nullable field inconsistencies
* missing columns in some partitions.

### Resolution

Before unioning datasets:

* `passenger_count` was cast to `double`,
* pickup timestamps were cast to `timestamp`,
* dropoff timestamps were cast to `timestamp`.

Datasets were merged using:

```python
unionByName(..., allowMissingColumns=True)
```

---

## Final Cleaning Summary

| Cleaning Step              | Records Removed |
| -------------------------- | --------------: |
| NULL passenger counts      |      23,716,389 |
| Passenger count = 0        |       2,764,050 |
| Timestamp anomalies        |             971 |
| Revenue outliers (> $1000) |             256 |
| Total Removed              |      26,481,666 |

---

## Final Analytical Dataset

Initial Dataset:

213,671,400 records

Final Dataset Used for Analysis:

187,189,734 records

---

## Key Lesson Learned

Real-world big data is rarely clean.

Significant effort was required to:

* validate assumptions,
* investigate anomalies,
* standardize schemas,
* identify corrupted records, and
* document every cleaning decision.

The quality of analytical insights depends heavily on the quality of the underlying data and the transparency of preprocessing steps.
