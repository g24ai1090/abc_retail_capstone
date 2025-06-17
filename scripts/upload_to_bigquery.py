from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import os

# -------------------- CONFIG --------------------
key_path = "credentials/abc-retail-capstone-d9ec3539cfc6.json"
project_id = "abc-retail-capstone"
dataset_id = "retail_analytics"
credentials = service_account.Credentials.from_service_account_file(key_path)
client = bigquery.Client(credentials=credentials, project=project_id)

# -------------------- UPLOAD LOCAL CSVs TO BIGQUERY TABLES --------------------
folder_path = "../data/transformed"
files_to_upload = {
    "sales_fact": {
        "file": os.path.join(folder_path, "sales_fact.csv"),
        "schema": [
            bigquery.SchemaField("invoice_no", "STRING"),
            bigquery.SchemaField("product_id", "STRING"),
            bigquery.SchemaField("date_id", "DATE"),
            bigquery.SchemaField("quantity", "INTEGER"),
            bigquery.SchemaField("revenue", "FLOAT"),
        ]
    },
    "product_dim": {
        "file": os.path.join(folder_path, "product_dim.csv"),
        "schema": [
            bigquery.SchemaField("product_id", "STRING"),
            bigquery.SchemaField("product_name", "STRING"),
            bigquery.SchemaField("unit_price", "FLOAT"),
        ]
    },
    "date_dim": {
        "file": os.path.join(folder_path, "date_dim.csv"),
        "schema": [
            bigquery.SchemaField("date_id", "DATE"),
            bigquery.SchemaField("year", "INTEGER"),
            bigquery.SchemaField("month", "INTEGER"),
            bigquery.SchemaField("day", "INTEGER"),
            bigquery.SchemaField("weekday", "STRING"),
            bigquery.SchemaField("is_weekend", "BOOLEAN"),
        ]
    },
}

for table_name, config in files_to_upload.items():
    file_path = config["file"]
    schema = config["schema"]
    table_id = f"{project_id}.{dataset_id}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        schema=schema,
        write_disposition="WRITE_TRUNCATE",
        max_bad_records=5,
    )

    with open(file_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)
        job.result()
        print(f"✅ Loaded data into {table_name} from {file_path}")
