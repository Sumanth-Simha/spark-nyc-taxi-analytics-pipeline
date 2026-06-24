# Category B Project Notes

## NYC Taxi Data Cleaning - Extreme Outlier Investigation Phase

Date: June 2026

---

# Phase Objective

The objective of Category B was to identify and investigate extreme numerical outliers that survived the initial integrity checks performed during Category A cleaning.

Unlike Category A, which focused on missing values and invalid records, Category B focused on identifying physically unrealistic values that could distort analytical results.

Examples included:

* Extremely large fares
* Extremely large total charges
* Extremely large trip distances

---

# Initial Dataset

Input Dataset:

artifacts/clean_category_A

Records Before Cleaning:

187,173,445

---

# Investigation Areas

The following anomaly categories were evaluated:

1. Fare Amount Outliers
2. Total Amount Outliers
3. Trip Distance Outliers

---

# Challenges Encountered

## Challenge 1: Choosing Realistic Thresholds

### Problem

The largest challenge was determining whether an extreme value represented:

* legitimate business activity
* luxury transportation
* data corruption
* system errors

For example:

Trip Amount = $8,000

could represent either:

* a corrupted record
* a rare billing event

### Solution

Conservative thresholds were selected to avoid removing valid transactions.

The investigation focused only on values that were clearly unrealistic.

### Lesson Learned

Aggressive filtering can remove legitimate business events and reduce dataset quality.

---

## Challenge 2: Defining Physical Limits

### Problem

The NYC Taxi dataset spans several years and contains hundreds of millions of records.

Some trips contained values that were technically possible according to the schema but physically unrealistic.

Examples:

* Distances exceeding hundreds of miles
* Extremely large fare values
* Extremely large total charges

### Solution

Business-based thresholds were introduced.

Records were flagged only when values exceeded realistic operational limits.

### Lesson Learned

Data validation should combine statistical analysis with domain knowledge.

---

## Challenge 3: Balancing Precision and Recall

### Problem

Removing too many records would risk losing valid data.

Removing too few records would leave corruption inside the dataset.

### Solution

Only extreme anomalies were removed.

Moderate outliers were retained for future analysis.

### Lesson Learned

Cleaning pipelines should prioritize data quality without unnecessarily reducing dataset size.

---

# Investigation Results

## Fare Amount Analysis

Rule Investigated:

fare_amount > 10,000

Records Found:

17

### Interpretation

Taxi fares exceeding $10,000 are not operationally realistic.

### Decision

REMOVE

Reason:

Likely data corruption or billing errors.

---

## Total Amount Analysis

Rule Investigated:

total_amount > 10,000

Records Found:

18

### Interpretation

Total trip charges above $10,000 are highly unlikely for standard taxi operations.

### Decision

REMOVE

Reason:

Likely corrupted financial records.

---

## Trip Distance Analysis

Rule Investigated:

trip_distance > 1,000 miles

Records Found:

535

### Interpretation

Trips exceeding 1,000 miles are not consistent with normal NYC taxi operations.

### Decision

REMOVE

Reason:

Likely GPS errors, unit conversion issues, or corrupted records.

---

# Approved Category B Cleaning Rules

Rule B1

fare_amount <= 10,000

Records Removed:

17

---

Rule B2

total_amount <= 10,000

Records Removed:

18

---

Rule B3

trip_distance <= 1,000

Records Removed:

535

---

# Cleaning Impact

Records Before Cleaning:

187,173,445

Records After Cleaning:

187,172,893

Records Removed:

552

Percentage Removed:

0.000295%

---

# Key Findings

1. Category A had already removed the majority of severe data quality issues.
2. Extreme numerical outliers were very rare.
3. Less than 0.001% of records violated Category B rules.
4. Distance anomalies represented the largest outlier category.
5. Financial anomalies were uncommon compared to operational anomalies.

---

# Engineering Takeaways

1. Large datasets often contain a small number of extreme corrupted records.
2. Outlier detection should be based on operational limits rather than arbitrary statistical thresholds.
3. Extreme values can significantly distort averages, revenue calculations, and visualizations.
4. Conservative filtering helps preserve legitimate business activity.
5. Outlier investigation should precede advanced analytics.

---

# Comparison with Other Cleaning Stages

Category A

Focus:
Data Integrity

Impact:
Millions of records removed

Examples:

* Null values
* Invalid passenger counts
* Invalid timestamps
* Corrupted years

---

Category B

Focus:
Extreme Numerical Outliers

Impact:
552 records removed

Examples:

* Fare > $10,000
* Total Amount > $10,000
* Distance > 1,000 miles

---

Category C

Focus:
Business Rule Validation

Impact:
778,140 records identified

Examples:

* Duration <= 0
* Passenger Count > 8
* Speed anomalies
* Fare-distance inconsistencies

---

# Phase Status

Category B Investigation:
COMPLETED

Category B Cleaning:
COMPLETED

Output Dataset:

artifacts/clean_category_B

Records Remaining:

187,172,893

---

# Final Assessment

Category B confirmed that the dataset contained very few extreme numerical outliers.

The low removal count indicates that most severe corruption had already been addressed during Category A cleaning.

This phase successfully eliminated unrealistic financial and distance values while preserving nearly all legitimate taxi transactions.

The resulting dataset provided a strong foundation for the business-rule investigations performed in Category C.
