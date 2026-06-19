import pandas as pd
import joblib
import json
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load train and test data
train = pd.read_parquet("data/processed/train.parquet")
test = pd.read_parquet("data/processed/test.parquet")

# Features and target
X_train = train.drop(columns=["yield_kg"])
y_train = train["yield_kg"]

X_test = test.drop(columns=["yield_kg"])
y_test = test["yield_kg"]

# Train Random Forest on TRAIN SET ONLY
rf = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train, y_train)

# Test predictions
pred = rf.predict(X_test)

# Metrics
mae = mean_absolute_error(y_test, pred)
rmse = mean_squared_error(y_test, pred) ** 0.5
r2 = r2_score(y_test, pred)

print(f"RF Test MAE : {mae:.2f} kg")
print(f"RF Test RMSE: {rmse:.2f} kg")
print(f"RF Test R²  : {r2:.3f}")

# Save metrics
Path("reports").mkdir(exist_ok=True)

rf_metrics = {
    "MAE": float(mae),
    "RMSE": float(rmse),
    "R2": float(r2)
}

with open("reports/random_forest_metrics.json", "w") as f:
    json.dump(rf_metrics, f, indent=4)

# Feature Importance Plot
Path("reports/figures").mkdir(parents=True, exist_ok=True)

importance = pd.Series(
    rf.feature_importances_,
    index=X_train.columns
).sort_values(ascending=False)

plt.figure(figsize=(6, 4))
importance.plot(kind="bar")
plt.title("Random Forest Feature Importance")
plt.ylabel("Importance")
plt.tight_layout()
plt.savefig(
    "reports/figures/rf_importance.png",
    dpi=300
)
plt.close()

# Save model
Path("models").mkdir(exist_ok=True)

joblib.dump(
    rf,
    "models/random_forest.joblib"
)

# Create comparison table
try:
    with open("reports/linear_regression_metrics.json") as f:
        linear = json.load(f)

    comparison = pd.DataFrame({
        "Metric": ["MAE", "RMSE", "R2"],
        "Linear Regression": [
            linear["test_mae"],
            linear["test_rmse"],
            linear["test_r2"]
        ],
        "Random Forest": [
            mae,
            rmse,
            r2
        ]
    })

    comparison.to_csv(
        "reports/model_comparison.csv",
        index=False
    )

    print("\nModel Comparison")
    print(comparison)

except FileNotFoundError:
    print("Linear regression metrics file not found.")

# Feature importance interpretation
print("\nFeature Importances:")
print(importance)

print("\nSaved files:")
print("- models/random_forest.joblib")
print("- reports/random_forest_metrics.json")
print("- reports/figures/rf_importance.png")
print("- reports/model_comparison.csv")