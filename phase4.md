# Phase 4: Outlier Detection & Extreme Value Investigation

## Objective

The goal of this phase was to identify abnormal, corrupted, and suspicious records within the NYC Yellow Taxi dataset before applying final cleaning rules.

Rather than arbitrarily removing records, the objective was to establish evidence-based thresholds through large-scale exploratory analysis.

---

# Dataset Overview

| Metric        |       Count |
| ------------- | ----------: |
| Raw Trips     | 213,671,400 |
| Cleaned Trips | 187,189,990 |

Initial cleaning removed records with:

* passenger_count <= 0
* Invalid pickup years outside 2021–2026

This reduced the dataset by approximately 26 million records.

---

# Outlier Investigation

The analysis focused on:

* Fare Amount
* Total Amount
* Trip Distance
* Tip Amount
* Trip Duration

Extreme values were investigated using percentile analysis, threshold analysis, and business-rule validation.

---

# Key Findings

## 1. Monetary Field Corruption

Several records contained impossible fare values despite very short trip distances.

Examples:

| Distance (Miles) |   Fare ($) |
| ---------------- | ---------: |
| 1.6              | 863,372.12 |
| 2.5              | 818,283.44 |
| 3.3              | 401,092.32 |

These records indicate severe corruption within monetary fields.

### Observation

The corruption appears systematic rather than random, suggesting possible:

* Overflow errors
* Data conversion issues
* Data ingestion anomalies

---

## 2. Distance Field Corruption

Extreme trip distances were discovered.

Examples:

| Distance (Miles) | Fare ($) |
| ---------------- | -------: |
| 186,967.57       |    11.68 |
| 184,340.80       |    38.08 |
| 164,072.79       |    16.00 |

These records are physically impossible.

A taxi trip spanning hundreds of thousands of miles while charging normal fares indicates corruption within the trip_distance field.

---

## 3. Distance Distribution Analysis

| Threshold      |  Trips |
| -------------- | -----: |
| > 50 Miles     | 30,562 |
| > 100 Miles    |  4,380 |
| > 500 Miles    |  1,073 |
| > 1,000 Miles  |    914 |
| > 10,000 Miles |    377 |

### Important Conclusion

Trips exceeding 100 miles cannot automatically be classified as invalid.

Long-distance taxi trips from NYC to nearby cities are operationally possible.

Examples include:

* Philadelphia
* Atlantic City
* Boston
* Washington DC

Therefore:

* Distances above 100 miles require investigation
* Distances in the thousands of miles are almost certainly corrupted

No final distance threshold was established during this phase.

---

## 4. Fare Distribution Analysis

| Threshold |  Trips |
| --------- | -----: |
| > $200    | 64,459 |
| > $500    |  2,407 |
| > $1,000  |    209 |
| > $5,000  |     84 |
| > $10,000 |     17 |

### Conclusion

The number of records decreases sharply at higher fare values.

Fares above several thousand dollars are likely corrupted and require removal during final cleaning.

---

## 5. Tip Distribution Analysis

| Threshold | Trips |
| --------- | ----: |
| > $100    | 2,363 |
| > $500    |    37 |
| > $1,000  |     4 |

### Conclusion

Tip data is generally clean.

Only a very small number of records contain extreme gratuities.

---

## 6. Zero-Distance Trip Investigation

| Metric                    |     Count |
| ------------------------- | --------: |
| Zero Distance Trips       | 2,400,946 |
| Zero Distance + Fare > 0  | 2,160,642 |
| Zero Distance + Total > 0 | 2,170,154 |

### Observation

This represents one of the largest remaining anomalies within the dataset.

Possible explanations include:

* GPS recording failures
* Meter recording issues
* Data entry errors
* Short trips rounded to zero

These records require separate investigation before removal.

---

## 7. Duration Analysis

| Condition           |   Trips |
| ------------------- | ------: |
| Negative Duration   |   4,107 |
| Duration > 5 Hours  | 178,417 |
| Duration > 10 Hours | 164,646 |
| Duration > 24 Hours |   1,092 |

### Conclusion

Negative-duration trips are invalid.

Trips exceeding 24 hours are highly suspicious and likely represent timestamp corruption.

---

## Invalid Transaction Detection

Business validation rules identified:

* Negative fares
* Negative totals
* Negative distances
* Zero distance with unrealistic charges
* Zero fare with unrealistic totals

### Result

| Metric        |     Count |
| ------------- | --------: |
| Invalid Trips | 2,452,917 |

These records were classified as corrupted transactions.

---

## Suspicious Transaction Detection

Suspicious trips were identified using:

* Extreme monetary values
* Extreme distances
* Excessive tip-to-fare ratios

### Result

| Metric           |  Count |
| ---------------- | -----: |
| Suspicious Trips | 30,319 |

These records were retained for further investigation.

---

# Phase 4 Outcome

Successfully identified:

* Large-scale monetary corruption
* Large-scale distance corruption
* 2.45 million invalid transactions
* 30,319 suspicious transactions
* Multiple extreme-value clusters requiring cleaning

Most importantly, this phase established an evidence-driven approach to data cleaning rather than relying on arbitrary thresholds.

---

# Next Phase

Phase 5: Data Cleaning & Trusted Dataset Construction

Objectives:

* Define final cleaning thresholds
* Remove corrupted records
* Handle invalid timestamps
* Investigate zero-distance trips
* Produce a high-quality analytical dataset for downstream business intelligence and revenue analysis
