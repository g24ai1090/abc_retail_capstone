# ABC Retail Corp - Data Inventory Report & Data Quality Assessment

---

## 1. Initial Data Inventory Report

| Column       | Data Type        | Non-Null Count | Unique Values | Sample Values                                               |
|--------------|------------------|----------------|---------------|------------------------------------------------------------|
| InvoiceNo    | object           | 541,909        | 25,900        | 536365, 536366, 536367                                     |
| StockCode    | object           | 541,909        | 4,070         | '85123A', 71053, '84406B'                                  |
| Description  | object           | 540,455        | 4,223         | 'WHITE HANGING HEART T-LIGHT HOLDER', 'WHITE METAL LANTERN', 'CREAM CUPID HEARTS COAT HANGER' |
| Quantity     | int64            | 541,909        | 722           | N/A                                                        |
| InvoiceDate  | datetime64[ns]   | 541,909        | 23,260        | N/A                                                        |
| UnitPrice    | float64          | 541,909        | 1,630         | N/A                                                        |
| CustomerID   | float64          | 406,829        | 4,372         | N/A                                                        |
| Country      | object           | 541,909        | 38            | 'United Kingdom', 'France', 'Australia'                    |

---

## 2. Initial Missing Values Summary

| Column       | Missing Count | Percentage Missing (%) |
|--------------|---------------|-----------------------|
| InvoiceNo    | 0             | 0.00                  |
| StockCode    | 0             | 0.00                  |
| Description  | 1,454         | 0.27                  |
| Quantity     | 0             | 0.00                  |
| InvoiceDate  | 0             | 0.00                  |
| UnitPrice    | 0             | 0.00                  |
| CustomerID   | 135,080       | 24.93                 |
| Country      | 0             | 0.00                  |

---

## 3. Initial Data Validity Checks

- Negative Quantity count: 10,624  
- Zero or negative UnitPrice count: 2,517  
- Returns (InvoiceNo starting with 'C'): 9,288  

---

## 4. Data Cleaning Summary

The following cleaning steps were applied to the dataset:

```python
df = df[~df['Description'].isnull()]
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
df = df.drop_duplicates()
df['Description'] = df['Description'].str.strip().str.upper()
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

df['InvoiceYear'] = df['InvoiceDate'].dt.year
df['InvoiceMonth'] = df['InvoiceDate'].dt.month
df['InvoiceDay'] = df['InvoiceDate'].dt.day
df['Weekday'] = df['InvoiceDate'].dt.day_name()
Removed rows with missing descriptions.

Excluded returns (InvoiceNo starting with 'C').

Filtered out rows with zero or negative Quantity or UnitPrice.

Dropped duplicates.

Standardized descriptions.

Created additional date columns (InvoiceYear, InvoiceMonth, InvoiceDay, Weekday).

5. Data Inventory & Quality After Cleaning
Column	Data Type	Non-Null Count	Unique Values	Sample Values
InvoiceNo	object	524,878	19,960	536365, 536366, 536367
StockCode	object	524,878	3,922	'85123A', 71053, '84406B'
Description	object	524,878	4,015	'WHITE HANGING HEART T-LIGHT HOLDER', 'WHITE METAL LANTERN', 'CREAM CUPID HEARTS COAT HANGER'
Quantity	int64	524,878	375	N/A
InvoiceDate	datetime64[ns]	524,878	18,499	N/A
UnitPrice	float64	524,878	1,291	N/A
CustomerID	float64	392,692	4,338	N/A
Country	object	524,878	38	'United Kingdom', 'France', 'Australia'
InvoiceYear	int32	524,878	2	N/A
InvoiceMonth	int32	524,878	12	N/A
InvoiceDay	int32	524,878	31	N/A
Weekday	object	524,878	6	'Wednesday', 'Thursday', 'Friday'

6. Missing Values Summary After Cleaning
Column	Missing Count	Percentage Missing (%)
InvoiceNo	0	0.00
StockCode	0	0.00
Description	0	0.00
Quantity	0	0.00
InvoiceDate	0	0.00
UnitPrice	0	0.00
CustomerID	132,186	25.18
Country	0	0.00
InvoiceYear	0	0.00
InvoiceMonth	0	0.00
InvoiceDay	0	0.00
Weekday	0	0.00

7. Data Validity Checks After Cleaning
Negative Quantity count: 0

Zero or negative UnitPrice count: 0

Returns (InvoiceNo starting with 'C'): 0

8. Next Steps
Proceed to Exploratory Data Analysis (EDA) to identify sales trends, seasonality, and product performance.

Feature engineering to prepare time series and aggregated sales features.

Build predictive sales forecasting models.

Design data warehouse schema for optimized storage and querying.

