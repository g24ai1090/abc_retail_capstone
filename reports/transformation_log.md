# ABC Retail Corp - Transformation Log

---

## ✅ Sprint 4: Data Transformation & Schema Design

### 1. Feature Engineering Summary

- Converted `InvoiceDate` to datetime and extracted:
  - `InvoiceYear`, `InvoiceMonth`, `InvoiceDay`, `Weekday`, `Hour`
- Created `Revenue` as `Quantity * UnitPrice`
- Generated `TotalPrice` and `WeeklyAvg` (moving average of revenue per customer)
- Ensured all identifiers (like `invoice_no`) were treated as string

---

### 2. Final Schema Design (Star Schema)

#### 📌 Fact Table: `sales_fact`
| Column       | Type    | Description                          |
|--------------|---------|--------------------------------------|
| invoice_no   | STRING  | Invoice number (as ID)               |
| product_id   | STRING  | Product SKU                          |
| date_id      | DATE    | Date of transaction                  |
| quantity     | INTEGER | Quantity sold                        |
| revenue      | FLOAT   | Revenue = quantity * unit_price      |

#### 📌 Dimension Table: `product_dim`
| Column       | Type    | Description          |
|--------------|---------|----------------------|
| product_id   | STRING  | Product SKU          |
| product_name | STRING  | Product description  |
| unit_price   | FLOAT   | Unit price           |

#### 📌 Dimension Table: `date_dim`
| Column       | Type    | Description         |
|--------------|---------|---------------------|
| date_id      | DATE    | Unique calendar date|
| year         | INTEGER | Year                |
| month        | INTEGER | Month               |
| day          | INTEGER | Day of month        |
| weekday      | STRING  | Day of week         |
| is_weekend   | BOOLEAN | Weekend flag        |

---

### 3. Aggregation Queries (BigQuery)

#### 1. `monthly_revenue_per_product`
- Calculates monthly revenue for each product
- Grouped by: `product_id`, `YEAR(date_id)`, `MONTH(date_id)`

#### 2. `top_10_products_by_quantity`
- Ranks products by total quantity sold
- Sorted descending, limited to top 10

#### 3. `daily_sales_trend`
- Computes daily revenue for business trend analysis

#### 4. `sales_fact_partitioned`
- Partitioned by `date_id`
- Clustered by `product_id`
- Optimized for query performance

---

### 4. Data Loading & Storage Optimization

- Transformed files exported as CSV:
  - `data/transformed/sales_fact.csv`
  - `data/transformed/product_dim.csv`
  - `data/transformed/date_dim.csv`
- Uploaded to BigQuery using Python scripts
- Schema enforced using `bigquery.SchemaField`
- Partitioned `sales_fact_partitioned` for performance

---

## 5. File Paths
- Transformed CSVs: `../data/transformed/*.csv`
- Script for upload: `scripts/upload_to_bigquery.py`

### 6. Challenges Resolved

- 🛠 `invoice_no` auto-casting to INTEGER: fixed by forcing string type in pandas
- 🛠 `date_id` TIMESTAMP vs DATE issue: fixed using `.dt.date` in pandas and `DATE(date_id)` in SQL
- ✅ Handled malformed rows by setting `max_bad_records = 5`
