import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

# -------------------- CONFIG --------------------
data_path = "data/transformed/sales_fact.csv"
output_path = "output/customer_segments.csv"
os.makedirs("output", exist_ok=True)

# -------------------- LOAD DATA --------------------
df = pd.read_csv(data_path)

# -------------------- AGGREGATE PER CUSTOMER/INVOICE --------------------
agged = df.groupby("invoice_no").agg({
    "Quantity": "sum",
    "Revenue": "sum"
}).reset_index()

# -------------------- CLUSTERING --------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(agged[['Quantity', 'Revenue']])

kmeans = KMeans(n_clusters=3, random_state=42)
agged['segment'] = kmeans.fit_predict(X_scaled)

# -------------------- SAVE OUTPUT --------------------
agged.to_csv(output_path, index=False)
print(f"Segments saved to {output_path}")
print(agged.head())
