# Phase 5A: Category A Cleaning Report

## Objective

The objective of Category A Cleaning was to permanently remove records that were objectively invalid and could not represent legitimate taxi trips under any realistic business scenario.

Unlike later cleaning phases, Category A focused only on records that were clearly corrupted and required no further investigation.

---

# Input Dataset

| Metric                  |       Count |
| ----------------------- | ----------: |
| Records Before Cleaning | 187,189,990 |

This dataset was the result of:

* Initial cleaning
* Outlier investigation
* Extreme value analysis

completed during previous project phases.

---

# Category A Rules

The following rules were selected because they represent impossible or invalid taxi trip conditions.

## Rule 1: Negative Trip Distance

Condition:

```python
trip_distance < 0
```

Reason:

A taxi trip cannot have a negative travel distance.

### Result

| Metric          | Count |
| --------------- | ----: |
| Removed Records |     0 |

No negative-distance records were found.

---

## Rule 2: Negative Tip Amount

Condition:

```python
tip_amount < 0
```

Reason:

Negative gratuities are not valid customer tips and were treated as corrupted transactions.

### Result

| Metric          |  Count |
| --------------- | -----: |
| Removed Records | 10,970 |

---

## Rule 3: Negative Trip Duration

Condition:

```python
trip_duration_min < 0
```

Reason:

Dropoff time occurring before pickup time indicates timestamp corruption.

### Result

| Metric          | Count |
| --------------- | ----: |
| Removed Records | 4,107 |

---

## Rule 4: Duration Greater Than 24 Hours

Condition:

```python
trip_duration_min > 1440
```

Reason:

Taxi trips lasting longer than one full day are highly unrealistic and likely caused by timestamp errors.

### Result

| Metric          | Count |
| --------------- | ----: |
| Removed Records | 1,092 |

---

## Rule 5: Extreme Distance Anomalies

Condition:

```python
trip_distance > 10000
```

Reason:

Trips exceeding 10,000 miles are physically impossible for NYC taxi operations.

Examples discovered during investigation included:

* 186,967 miles
* 184,340 miles
* 164,072 miles

These values indicated severe corruption within the distance field.

### Result

| Metric          | Count |
| --------------- | ----: |
| Removed Records |   377 |

---

# Cleaning Summary

| Rule                    | Records Removed |
| ----------------------- | --------------: |
| Negative Distance       |               0 |
| Negative Tip            |          10,970 |
| Negative Duration       |           4,107 |
| Duration > 24 Hours     |           1,092 |
| Distance > 10,000 Miles |             377 |
| **Total Removed**       |      **16,545** |

---

# Dataset After Cleaning

| Metric                  |       Count |
| ----------------------- | ----------: |
| Records Before Cleaning | 187,189,990 |
| Records After Cleaning  | 187,173,445 |
| Records Removed         |      16,545 |

Retention Rate:

```text
99.991%
```

Only a very small fraction of records were removed, ensuring that data quality improved without significantly reducing dataset size.

---

# Key Findings

### 1. Distance Corruption Was Extreme Rather Than Frequent

No negative-distance records existed, but a small number of records contained impossible distances exceeding 10,000 miles.

This indicates that distance corruption occurred through abnormal spikes rather than sign errors.

---

### 2. Timestamp Issues Were Present

More than 5,000 records contained invalid durations caused by timestamp inconsistencies.

These records were safely removed.

---

### 3. Negative Tips Were the Largest Source of Invalid Data

A total of 10,970 records contained negative gratuity values.

These represented the largest Category A anomaly group.

---

# Outcome

Category A Cleaning successfully removed records that were objectively invalid and required no business interpretation.

The resulting dataset contains:

```text
187,173,445 trusted records
```

and serves as the foundation for Category B investigation and advanced cleaning.

The next phase will focus on reviewing extreme monetary values and long-distance trips that appear suspicious but require evidence before removal.
