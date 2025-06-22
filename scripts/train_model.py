import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import os

# -------------------- CONFIG --------------------
data_path = "output/daily_sales_trend.csv"
model_path = "models/daily_revenue_model.pkl"
prediction_output = "output/model_predictions.csv"

os.makedirs("models", exist_ok=True)
os.makedirs("output", exist_ok=True)

# -------------------- LOAD DATA --------------------
df = pd.read_csv(data_path)
df['date_id'] = pd.to_datetime(df['date_id'])
df['date_ordinal'] = df['date_id'].map(pd.Timestamp.toordinal)

# -------------------- MODEL TRAINING --------------------
X = df[['date_ordinal']]
y = df['daily_revenue']
X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

model = LinearRegression()
model.fit(X_train, y_train)

# -------------------- PREDICTION & EVALUATION --------------------
y_pred = model.predict(X_test)
rmse = root_mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("RMSE:", rmse)
print("R2 Score:", r2)

# -------------------- SAVE MODEL --------------------
joblib.dump(model, model_path)
print(f"Model saved to {model_path}")

# -------------------- EXPORT PREDICTIONS --------------------
results = pd.DataFrame({
    "actual": y_test.values,
    "predicted": y_pred
})
results.to_csv(prediction_output, index=False)
print(f"Predictions saved to {prediction_output}")

# -------------------- PLOT RESULTS --------------------
plt.figure(figsize=(10, 5))
plt.plot(y_test.values, label='Actual')
plt.plot(y_pred, label='Predicted')
plt.title('Actual vs Predicted Daily Revenue')
plt.legend()
plt.show()
