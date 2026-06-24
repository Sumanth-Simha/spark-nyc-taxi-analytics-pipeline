# Category C Project Notes

## NYC Taxi Data Cleaning - Business Rule Validation Phase

Date: June 2026

---

# Phase Objective

The goal of Category C was to investigate business-rule violations and logical inconsistencies that remained after Category A and Category B cleaning.

This phase focused on determining whether taxi trips were operationally valid rather than simply statistically reasonable.

---

# Initial Dataset

Input Dataset:

artifacts/clean_category_B

Records:

187,172,893

---

# Challenges Encountered

## Challenge 1: Spark ANSI Division By Zero Error

### Problem

During speed analysis, Spark repeatedly failed with:

DIVIDE_BY_ZERO

Error Location:

investigate_category_C.py

Speed Formula:

speed_mph = trip_distance / duration_hours

### Root Cause

The dataset contained hundreds of thousands of trips with invalid durations.

Examples included:

* pickup time after dropoff time
* zero duration trips
* corrupted timestamps

These records caused duration_hours to become zero.

When Spark attempted to calculate speed, ANSI mode terminated the job.

### Solution

Implemented safe division using:

try_divide()

and explicitly filtered:

duration_minutes > 0

before speed calculations.

### Lesson Learned

Large datasets frequently contain logical inconsistencies that may not be discovered until derived metrics are calculated.

---

## Challenge 2: Misleading Speed Anomalies

### Problem

Initial assumption:

Speed > 150 mph = corrupted data

However, many trips had extremely short durations.

Example:

Distance = 1 mile
Duration = 10 seconds

This produces mathematically impossible speeds while not necessarily indicating distance corruption.

### Solution

Decided not to automatically remove high-speed records.

Further investigation is required before defining a cleaning rule.

### Lesson Learned

Business context is more important than raw mathematical thresholds.

---

## Challenge 3: Tip Ratio Explosion

### Problem

Large numbers of trips were identified where:

Tip > Fare

or

Tip > 5 × Fare

Initial assumption suggested potential corruption.

### Investigation

Many records contained very small fares.

Example:

Fare = $1
Tip = $10

Ratio becomes extreme despite representing a valid transaction.

### Solution

No cleaning rule applied.

### Lesson Learned

Ratio-based anomaly detection can generate misleading results when denominators are small.

---

## Challenge 4: Distance vs Fare Inconsistency

### Problem

More than 2 million records had:

Distance = 0
Fare > 0

Initial assumption suggested corrupted GPS data.

### Investigation

Several legitimate explanations exist:

* waiting charges
* airport fees
* cancellation fees
* minimum fare charges
* administrative adjustments

### Solution

Records retained.

### Lesson Learned

Business processes often create patterns that appear anomalous from a purely technical perspective.

---

# Major Findings

## Duration Analysis

Duration <= 0

Records Found:

777,926

Decision:

REMOVE

Reason:

Physically impossible trips.

---

## Speed Analysis

Speed > 150 mph

Records Found:

72,781

Decision:

KEEP FOR NOW

Reason:

Requires further investigation.

---

## Distance vs Fare

Distance = 0 & Fare > 0

Records Found:

2,160,315

Decision:

KEEP

Reason:

Likely valid business scenarios.

---

## Passenger Count

Passenger Count > 8

Records Found:

214

Extreme Values Found:

96 passengers
112 passengers

Decision:

REMOVE

Reason:

Operationally impossible.

---

## Tip Analysis

Tip > 5x Fare

Records Found:

2,291,713

Decision:

KEEP

Reason:

Caused primarily by very small fare values.

---

# Approved Category C Cleaning Rules

Rule C1

duration_minutes > 0

Records Removed:

777,926

---

Rule C2

passenger_count <= 8

Records Removed:

214

---

# Estimated Category C Impact

Total Records Removed:

778,140

Approximate Percentage Removed:

0.42%

---

# Engineering Takeaways

1. Logical validation discovers issues that statistical outlier detection misses.
2. Derived metrics often reveal hidden data quality problems.
3. Business understanding is critical before removing records.
4. Safe mathematical operations are essential when processing large-scale datasets.
5. Large datasets frequently contain edge cases that only appear after multiple cleaning stages.

---

# Phase Status

Category C Investigation:
COMPLETED

Category C Cleaning:
NEXT PHASE

Next File:

src/clean_category_C.py

Output Dataset:

artifacts/clean_category_C
