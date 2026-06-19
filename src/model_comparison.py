import pandas as pd
import matplotlib.pyplot as plt
import json
from pathlib import Path
from joblib import load
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load test data
test = pd.read_parquet("data/processed/test.parquet")

X_test = test.drop(columns=["yield_kg"])
y_test = test["yield_kg"]

# Load models
linear_model = load("models/linear_regression.joblib")
rf_default = load("models/random_forest.joblib")
rf_tuned = load("models/random_forest_tuned.joblib")

# Predictions
pred_linear = linear_model.predict(X_test)
pred_rf = rf_default.predict(X_test)
pred_rf_tuned = rf_tuned.predict(X_test)

# Metrics function
def get_metrics(y_true, y_pred):
    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": mean_squared_error(y_true, y_pred) ** 0.5,
        "R2": r2_score(y_true, y_pred)
    }

linear_metrics = get_metrics(y_test, pred_linear)
rf_metrics = get_metrics(y_test, pred_rf)
rf_tuned_metrics = get_metrics(y_test, pred_rf_tuned)

# Comparison table
results = pd.DataFrame({
    "Model": [
        "Linear Regression",
        "Random Forest",
        "Tuned Random Forest"
    ],
    "Test MAE": [
        linear_metrics["MAE"],
        rf_metrics["MAE"],
        rf_tuned_metrics["MAE"]
    ],
    "Test RMSE": [
        linear_metrics["RMSE"],
        rf_metrics["RMSE"],
        rf_tuned_metrics["RMSE"]
    ],
    "Test R2": [
        linear_metrics["R2"],
        rf_metrics["R2"],
        rf_tuned_metrics["R2"]
    ],
    "Interpretability": [
        "High",
        "Medium",
        "Low"
    ]
})

print(results)

Path("reports").mkdir(exist_ok=True)
results.to_csv(
    "reports/model_comparison.csv",
    index=False
)

# Champion model = tuned RF
champion = rf_tuned
pred = pred_rf_tuned

# Predicted vs Actual plot
Path("reports/figures").mkdir(
    parents=True,
    exist_ok=True
)

plt.figure(figsize=(6, 5))
plt.scatter(y_test, pred, alpha=0.6)
plt.plot(
    [y_test.min(), y_test.max()],
    [y_test.min(), y_test.max()],
    "r--"
)
plt.xlabel("Actual Yield (kg)")
plt.ylabel("Predicted Yield (kg)")
plt.title("Champion Model: Predicted vs Actual")
plt.tight_layout()
plt.savefig(
    "reports/figures/pred_vs_actual.png",
    dpi=150
)
plt.close()

print("Comparison saved.")
print("Plot saved.")