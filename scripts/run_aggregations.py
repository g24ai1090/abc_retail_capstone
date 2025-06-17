from google.cloud import bigquery
from google.oauth2 import service_account
import os
import pandas as pd

# -------------------- CONFIG --------------------
key_path = "credentials/abc-retail-capstone-d9ec3539cfc6.json"
project_id = "abc-retail-capstone"
dataset_id = "retail_analytics"
credentials = service_account.Credentials.from_service_account_file(key_path)
client = bigquery.Client(credentials=credentials, project=project_id)

# -------------------- AGGREGATION QUERIES --------------------
queries = {
    "monthly_revenue_per_product": {
        "sql": """
            CREATE OR REPLACE TABLE `abc-retail-capstone.retail_analytics.monthly_revenue_per_product` AS
            SELECT
                product_id,
                EXTRACT(YEAR FROM date_id) AS year,
                EXTRACT(MONTH FROM date_id) AS month,
                SUM(revenue) AS monthly_revenue
            FROM `abc-retail-capstone.retail_analytics.sales_fact`
            GROUP BY product_id, year, month
        """,
        "output_query": "SELECT * FROM `abc-retail-capstone.retail_analytics.monthly_revenue_per_product` LIMIT 10",
        "output_file": "output/monthly_revenue_per_product.csv"
    },

    "top_10_products_by_quantity": {
        "sql": """
            CREATE OR REPLACE TABLE `abc-retail-capstone.retail_analytics.top_10_products_by_quantity` AS
            SELECT
                product_id,
                SUM(quantity) AS total_quantity
            FROM `abc-retail-capstone.retail_analytics.sales_fact`
            GROUP BY product_id
            ORDER BY total_quantity DESC
            LIMIT 10
        """,
        "output_query": "SELECT * FROM `abc-retail-capstone.retail_analytics.top_10_products_by_quantity`",
        "output_file": "output/top_10_products_by_quantity.csv"
    },

    "daily_sales_trend": {
        "sql": """
            CREATE OR REPLACE TABLE `abc-retail-capstone.retail_analytics.daily_sales_trend` AS
            SELECT
                date_id,
                SUM(revenue) AS daily_revenue
            FROM `abc-retail-capstone.retail_analytics.sales_fact`
            GROUP BY date_id
            ORDER BY date_id
        """,
        "output_query": "SELECT * FROM `abc-retail-capstone.retail_analytics.daily_sales_trend` LIMIT 10",
        "output_file": "output/daily_sales_trend.csv"
    },

    "partitioned_sales_fact": {
        "sql": """
            CREATE OR REPLACE TABLE `abc-retail-capstone.retail_analytics.sales_fact_partitioned`
            PARTITION BY date_id
            CLUSTER BY product_id
            AS
            SELECT
              invoice_no,
              product_id,
              date_id,
              quantity,
              revenue
            FROM `abc-retail-capstone.retail_analytics.sales_fact`
            WHERE date_id IS NOT NULL
        """,
        "output_query": None,
        "output_file": None
    }
}

os.makedirs("output", exist_ok=True)

# -------------------- RUN QUERIES AND EXPORT OUTPUT --------------------
for query_name, content in queries.items():
    print(f"\nRunning query: {query_name}")
    job = client.query(content["sql"])
    job.result()
    print(f"✅ Completed: {query_name}")

    if content["output_query"] and content["output_file"]:
        print(f"   Exporting output to: {content['output_file']}")
        output_job = client.query(content["output_query"])
        output_df = output_job.to_dataframe()
        output_df.to_csv(content["output_file"], index=False)
        print(output_df)