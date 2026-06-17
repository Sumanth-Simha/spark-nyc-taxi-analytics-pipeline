# Phase 2: Outlier Detection and Investigation Notes

## Objective

The goal of this phase was not to immediately remove unusual observations from the NYC Taxi dataset, but to understand the nature of extreme values and determine whether they represented:

* Legitimate but rare trips,
* Business-related events such as refunds,
* Suspicious transactions requiring investigation,
* Or clearly corrupted records that should be removed.

This distinction is important because blindly removing statistical outliers can lead to the loss of meaningful information.

---

# Dataset Overview

After combining all monthly NYC Yellow Taxi datasets from 2021 to 2026 and applying basic cleaning rules, the dataset contained:

* **Original Trips:** 213,671,400
* **Trips After Basic Cleaning:** 187,189,990

Basic cleaning included:

* Removing records with `passenger_count <= 0`
* Restricting trips to the period between 2021 and 2026

---

# Initial Outlier Detection

Extreme value analysis was performed on the following variables:

* `fare_amount`
* `total_amount`
* `trip_distance`
* `tip_amount`

The 99th and 99.9th percentiles were calculated.

## Results

| Variable      | 99th Percentile | 99.9th Percentile |
| ------------- | --------------- | ----------------- |
| Fare Amount   | 73.00           | 863,372.12        |
| Total Amount  | 102.25          | 863,380.37        |
| Trip Distance | 20.05           | 186,967.57        |
| Tip Amount    | 17.19           | 1,400.16          |

---

# Major Discovery 1: Percentiles Were Corrupted

The calculated 99.9th percentile values were unrealistic.

Examples include:

* Trip distance: **186,967.57 miles**
* Fare amount: **$863,372.12**
* Total amount: **$863,380.37**

These values are impossible within the context of NYC taxi operations.

For perspective:

* The circumference of Earth is approximately **24,900 miles**.
* Some recorded taxi trips exceeded this by several multiples.

This indicated that the dataset contained severe data corruption.

## Conclusion

Statistical thresholds derived directly from the raw dataset could not be trusted.

Domain knowledge had to be applied before further outlier analysis.

---

# Major Discovery 2: Impossible High Charges

Several trips exhibited extremely large charges despite very short distances.

Examples:

| Distance  | Fare        | Total       |
| --------- | ----------- | ----------- |
| 1.6 miles | $863,372.12 | $863,380.37 |
| 2.5 miles | $818,283.44 | $818,286.74 |
| 3.3 miles | $401,092.32 | $401,095.62 |

These records clearly represent corrupted observations.

## Conclusion

Records containing extremely large monetary values should be classified as corrupted data.

---

# Major Discovery 3: Impossible Distances

Examples included:

| Distance         | Total Amount |
| ---------------- | ------------ |
| 186,967.57 miles | $15.14       |
| 184,340.80 miles | $41.38       |
| 164,072.79 miles | $22.54       |

These observations violate basic operational reality.

No NYC taxi trip can span such distances while incurring minimal charges.

## Conclusion

Distance-based corruption exists within the dataset and requires explicit filtering rules.

---

# Major Discovery 4: Negative Charges May Represent Refunds

Initial invalid-trip detection identified:

* **2,452,917 records**

containing negative fare or total values.

Examples:

| Fare    | Total   |
| ------- | ------- |
| -41.50  | -45.30  |
| -16.00  | -19.80  |
| -100.00 | -100.30 |

At first glance these appeared invalid.

However, further consideration suggests these records may represent:

* Refunds,
* Charge reversals,
* Transaction corrections,
* Voided payments.

## Conclusion

Negative monetary values should not automatically be deleted.

They may contain meaningful business information and should instead be isolated into a separate category.

---

# Major Discovery 5: Extremely High Tips

Examples included:

| Fare   | Tip       | Total     |
| ------ | --------- | --------- |
| $47.00 | $1,400.16 | $1,447.96 |
| $13.00 | $1,393.86 | $1,410.66 |
| $4.50  | $999.99   | $1,008.29 |

These observations are unusual.

However, unlike impossible distances and charges, they remain theoretically possible.

Human behavior occasionally produces extreme outcomes.

## Conclusion

Large tips should be classified as suspicious rather than corrupted.

---

# Revised Understanding of Outliers

The investigation demonstrated that not all outliers are equal.

The original assumption:

> Outliers are errors and should be removed.

was replaced with a more nuanced understanding:

> Outliers must be interpreted using both statistical evidence and domain knowledge.

---

# Proposed Classification Framework

## 1. Corrupted Trips

Characteristics:

* Impossible distances,
* Unrealistically large fares,
* Unrealistically large total amounts.

Action:

* Remove from the analytical dataset.

---

## 2. Refund Trips

Characteristics:

* Negative fare amounts,
* Negative total amounts.

Action:

* Preserve separately as business events.

---

## 3. Suspicious Trips

Characteristics:

* Extremely high tips,
* Unusual but theoretically possible transactions.

Action:

* Preserve separately for investigation.

---

## 4. Clean Trips

Characteristics:

* Trips not belonging to any of the above categories.

Action:

* Use for downstream analytics and reporting.

---

# Key Lesson Learned

The most important lesson from this phase was that:

> Statistical methods alone are insufficient for data cleaning.

Extreme values can distort percentile calculations and lead to misleading conclusions.

Effective data quality assessment requires a combination of:

* Statistical techniques,
* Domain knowledge,
* Human interpretation.

This phase transformed the project from a simple exercise in outlier removal into a data quality investigation aimed at preserving meaningful information while eliminating true corruption.

---

# Next Steps

1. Quantify the number of:

   * Corrupted trips,
   * Refund trips,
   * Suspicious trips.

2. Establish domain-based thresholds.

3. Develop `clean_data.py` using these validated rules.

4. Perform EDA on the resulting clean dataset.

This approach ensures that the final analytical dataset is both statistically sound and operationally meaningful.
