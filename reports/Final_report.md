# ABC Retail Corp - Capstone Project Final Report (Group 2)

## Project Title: Retail Sales Optimization for ABC Retail Corp

## Team Members:

* Manisha Bhalla (G24AI1073)
* Nupur Gupta (G24AI1090)
* Surbhi Shukla (G24AI1014)
* Richa Sharma (G24AI1029)

---

## 1. Introduction

Our goal was to analyze retail transaction data and build insights, models, and visualizations that could help ABC Retail Corp improve sales strategy, inventory planning, and customer engagement.

We used the Online Retail dataset from the UCI Machine Learning Repository.

---

## 2. Tools & Technologies

* Python, Pandas, NumPy
* Google BigQuery
* Streamlit
* scikit-learn, XGBoost
* Matplotlib, Seaborn
* GitHub, Trello (JIRA Board)

---

## 3. Project Phases

### Sprint 1: Understanding the Data

* Explored structure and types of attributes
* Identified missing values, duplicates, and outliers

### Sprint 2: Data Cleaning

* Removed canceled invoices and null CustomerIDs
* Converted datatypes, removed duplicates
* Created new column: `TotalPrice = Quantity * UnitPrice`

### Sprint 3: Data Ingestion

* Uploaded cleaned dataset to SQLite and Google BigQuery
* Connected BigQuery from Python using service account

### Sprint 4: Transformation & Schema Design

* Created a star schema with:

  * `sales_fact`
  * `product_dim`
  * `date_dim`
* Engineered new features (date breakdowns, revenue)
* Exported final CSVs and loaded to BigQuery

### Sprint 5: Modeling & Segmentation

* Baseline model: Linear Regression to predict daily revenue
* Improved model: XGBoost for product-level quantity prediction
* Customer segmentation using KMeans (based on revenue and quantity)
* Evaluated models using RMSE and R² score

### Sprint 6: Dashboard & Final Reporting

* Built an interactive dashboard using Streamlit
* Added revenue trends, top products, and customer segments
* Documented all key steps in this report
* Slide deck created for final presentation

---

## 4. Key Insights

* Revenue was highest during Nov-Dec period, likely due to holiday shopping
* Top 10 products contributed a large portion of sales volume
* Weekends showed lower order volume than weekdays
* Identified 3 customer segments with different purchasing behaviors

---

## 5. Deliverables

* Cleaned and transformed data (`data/transformed/`)
* Models and evaluation results (`models/`, `output/`)
* Dashboard (`scripts/dashboard_app.py`)
* Final slide deck (`presentations/ABC_Retail_Presentation.pptx`)
* GitHub Repo: https://github.com/g24ai1090/abc_retail_capstone

---

## 6. Next Steps / Recommendations

* Add more detailed product metadata (e.g., category, brand)
* Include time-series forecasting models like Prophet
* Use Streamlit Cloud for publishing the dashboard publicly
* Enhance segmentation by adding RFM metrics

---

## 7. Acknowledgments

Thanks to our guide Ashutosh and the faculty team for their continued support and feedback throughout the project.

---

**Submitted by:**
*Team Group 2 - ABC Retail Capstone*
*June 2025*
