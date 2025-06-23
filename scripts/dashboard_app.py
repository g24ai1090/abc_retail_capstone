import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
sales = pd.read_csv("output/daily_sales_trend.csv")
segments = pd.read_csv("output/customer_segments.csv")

# Dashboard UI
st.title("ABC Retail Sales Dashboard")

tab1, tab2, tab3 = st.tabs(["Revenue Trends", "Top Products", "Customer Segments"])

with tab1:
    st.subheader("Daily Revenue")
    st.line_chart(sales.set_index("date_id")["daily_revenue"])

with tab2:
    st.subheader("Top 10 Products by Quantity")
    top_products = pd.read_csv("output/top_10_products_by_quantity.csv")
    st.bar_chart(top_products.set_index("product_id"))

with tab3:
    st.subheader("Customer Segments")
    st.dataframe(segments)
