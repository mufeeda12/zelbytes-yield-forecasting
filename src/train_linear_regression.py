import pandas as pd
import json
import joblib
from pathlib import Path

from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# Load processed datasets
train = pd.read_parquet("data/processed/train.parquet")
test = pd.read_parquet("data/processed/test.parquet")

# Features and target
X_train = train.drop(columns=["yield_kg"])
y_train = train["yield_kg"]

X_test = test.drop(columns=["yield_kg"])
y_test = test["yield_kg"]

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
train_pred = model.predict(X_train)
test_pred = model.predict(X_test)

# Metrics
metrics = {
    "train_mae": mean_absolute_error(y_train, train_pred),
    "train_rmse": mean_squared_error(
        y_train,
        train_pred
    ) ** 0.5,
    "train_r2": r2_score(y_train, train_pred),

    "test_mae": mean_absolute_error(y_test, test_pred),
    "test_rmse": mean_squared_error(
        y_test,
        test_pred
    ) ** 0.5,
    "test_r2": r2_score(y_test, test_pred)
}

# Print metrics
print("\n=== Linear Regression Results ===")
for k, v in metrics.items():
    print(f"{k}: {v:.4f}")

# Coefficients
coef_df = pd.DataFrame({
    "feature": X_train.columns,
    "coefficient": model.coef_
})

print("\nCoefficients:")
print(coef_df)

# Create folders
Path("models").mkdir(exist_ok=True)
Path("reports").mkdir(exist_ok=True)

# Save model
joblib.dump(
    model,
    "models/linear_regression.joblib"
)

# Save metrics
with open(
    "reports/linear_regression_metrics.json",
    "w"
) as f:
    json.dump(metrics, f, indent=4)

# Save coefficients
coef_df.to_csv(
    "reports/linear_regression_coefficients.csv",
    index=False
)

print("\nModel saved successfully.")