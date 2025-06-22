import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error, r2_score
import os

# -------------------- CONFIG --------------------
data_path = "data/transformed/sales_fact.csv"
os.makedirs("models", exist_ok=True)

# -------------------- LOAD & PREP DATA --------------------
df = pd.read_csv(data_path)
df['date_id'] = pd.to_datetime(df['date_id'])
df['day'] = df['date_id'].dt.day
df['month'] = df['date_id'].dt.month
df['weekday'] = df['date_id'].dt.dayofweek

# Encode product_id
df['product_id'] = df['product_id'].astype('category').cat.codes

# Features and Target
features = ['product_id', 'day', 'month', 'weekday']
X = df[features]
y = df['Quantity']

# -------------------- TRAIN/TEST SPLIT --------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# -------------------- XGBOOST MODEL --------------------
model = xgb.XGBRegressor()
model.fit(X_train, y_train)

# -------------------- EVALUATE --------------------
y_pred = model.predict(X_test)
rmse = root_mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("XGBoost RMSE:", rmse)
print("XGBoost R2 Score:", r2)