from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import os

# -------------------- CONFIG --------------------
key_path = "credentials/abc-retail-capstone-d9ec3539cfc6.json"
project_id = "abc-retail-capstone"
dataset_id = f"{project_id}.retail_analytics"

# -------------------- AUTH ----------------------
credentials = service_account.Credentials.from_service_account_file(key_path)
client = bigquery.Client(credentials=credentials, project=project_id)

# -------------------- LOAD CLEANED DATA --------
os.makedirs("../data/transformed", exist_ok=True)
df = pd.read_csv("../data/cleaned/online_retail_cleaned.csv")

# -------------------- FEATURE ENGINEERING -------
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['year'] = df['InvoiceDate'].dt.year
df['month'] = df['InvoiceDate'].dt.month
df['day'] = df['InvoiceDate'].dt.day
df['weekday'] = df['InvoiceDate'].dt.day_name()
df['InvoiceYear'] = df['InvoiceDate'].dt.year
df['InvoiceMonth'] = df['InvoiceDate'].dt.month
df['InvoiceDay'] = df['InvoiceDate'].dt.day
df['Weekday'] = df['InvoiceDate'].dt.day_name()
df['Hour'] = df['InvoiceDate'].dt.hour
df['Revenue'] = df['Quantity'] * df['UnitPrice']
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
df['WeeklyAvg'] = df.groupby('CustomerID')['Revenue'].transform(lambda x: x.rolling(7, min_periods=1).mean())

# -------------------- BUILD DIM TABLES ----------
# Date Dimension
date_dim = df[['InvoiceDate', 'year', 'month', 'day', 'weekday']].drop_duplicates().copy()
date_dim['is_weekend'] = date_dim['weekday'].isin(['Saturday', 'Sunday'])
date_dim.rename(columns={'InvoiceDate': 'date_id'}, inplace=True)
date_dim['date_id'] = pd.to_datetime(date_dim['date_id']).dt.date

# Product Dimension
product_dim = df[['StockCode', 'Description', 'UnitPrice']].drop_duplicates().copy()
product_dim.rename(columns={
    'StockCode': 'product_id',
    'Description': 'product_name',
    'UnitPrice': 'unit_price'
}, inplace=True)

# Sales Fact Table
sales_fact = df[['InvoiceNo', 'StockCode', 'InvoiceDate', 'Quantity', 'Revenue']].copy()
sales_fact.rename(columns={
    'InvoiceNo': 'invoice_no',
    'StockCode': 'product_id',
    'InvoiceDate': 'date_id'
}, inplace=True)
sales_fact['date_id'] = pd.to_datetime(sales_fact['date_id']).dt.date
sales_fact['invoice_no'] = sales_fact['invoice_no'].astype(str)

# -------------------- SAVE TRANSFORMED CSVs ------
sales_fact.to_csv("../data/transformed/sales_fact.csv", index=False)
product_dim.to_csv("../data/transformed/product_dim.csv", index=False)
date_dim.to_csv("../data/transformed/date_dim.csv", index=False)
print("✅ Transformed CSVs saved in data/transformed/")

# -------------------- CREATE DATASET -------------
dataset = bigquery.Dataset(dataset_id)
dataset.location = "US"
try:
    dataset = client.create_dataset(dataset, timeout=30)
    print(f"✅ Dataset created: {dataset.dataset_id}")
except Exception as e:
    print(f"⚠️ Dataset creation skipped or failed: {e}")

# -------------------- CREATE TABLE SCHEMA ---------
table_schemas = {
    "sales_fact": [
        bigquery.SchemaField("invoice_no", "STRING"),
        bigquery.SchemaField("product_id", "STRING"),
        bigquery.SchemaField("date_id", "DATE"),
        bigquery.SchemaField("quantity", "INTEGER"),
        bigquery.SchemaField("revenue", "FLOAT")
    ],
    "product_dim": [
        bigquery.SchemaField("product_id", "STRING"),
        bigquery.SchemaField("product_name", "STRING"),
        bigquery.SchemaField("unit_price", "FLOAT")
    ],
    "date_dim": [
        bigquery.SchemaField("date_id", "DATE"),
        bigquery.SchemaField("year", "INTEGER"),
        bigquery.SchemaField("month", "INTEGER"),
        bigquery.SchemaField("day", "INTEGER"),
        bigquery.SchemaField("weekday", "STRING"),
        bigquery.SchemaField("is_weekend", "BOOLEAN")
    ]
}

# -------------------- CREATE TABLES ---------------
for table_name, schema in table_schemas.items():
    table_ref = f"{dataset_id}.{table_name}"
    table = bigquery.Table(table_ref, schema=schema)
    try:
        client.create_table(table)
        print(f"✅ Table created: {table_name}")
    except Exception as e:
        print(f"⚠️ Could not create {table_name}: {e}")