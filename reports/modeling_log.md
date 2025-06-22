# ABC Retail Capstone - Modeling Log (Sprint 5)

## Overview

This document outlines the modeling process performed in Sprint 5, including the baseline model, improvements, validation, segmentation, and output files.

---

## 1. Baseline Predictive Model (Linear Regression)

* **File**: `scripts/train_model.py`
* **Data Used**: `output/daily_sales_trend.csv`
* **Target Variable**: `daily_revenue`
* **Feature**: `date_ordinal` (converted from `date_id`)
* **Model**: `LinearRegression()`
* **Metrics**:

  * Root Mean Squared Error (RMSE)
  * R² Score
* **Outputs**:

  * `models/daily_revenue_model.pkl`
  * `output/model_predictions.csv`
  * Matplotlib plot of actual vs predicted

---

## 2. Improved Model (XGBoost)

* **File**: `scripts/improve_model.py`
* **Data Used**: `data/transformed/sales_fact.csv`
* **Target Variable**: `quantity`
* **Features**:

  * Encoded `product_id`
  * `day`, `month`, `weekday`
* **Model**: `XGBRegressor()`
* **Metrics**:

  * RMSE
  * R² Score

---

## 3. Model Validation

* Evaluation metrics printed for both models
* `train_model.py` includes visualizations
* `improve_model.py` focuses on quantity prediction accuracy

---

## 4. Segmentation (KMeans Clustering)

* **File**: `scripts/segment_customers.py`
* **Data Used**: `data/transformed/sales_fact.csv`
* **Aggregation**: by `invoice_no` on `quantity` and `revenue`
* **Clustering**:

  * Scaled with `StandardScaler`
  * `KMeans(n_clusters=3)`
* **Output**:

  * Segmented data saved as `output/customer_segments.csv`

---

## Final Notes

* The baseline and improved models provide two different perspectives: revenue forecasting and product demand.
* Segmentation helps group customer behaviors for future targeted marketing or pricing strategies.
* All scripts are modular and follow a clear pipeline for reproducibility.

---

**Prepared By**: Team ABC Retail
**Date**: 2025-06-17
