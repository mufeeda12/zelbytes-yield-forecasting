import pandas as pd
import joblib
import matplotlib.pyplot as plt
from pathlib import Path

# Create output folder
Path("reports/figures").mkdir(parents=True, exist_ok=True)

# Load test dataset
test = pd.read_parquet("data/processed/test.parquet")

# Features and target
X_test = test.drop(columns=["yield_kg"])
y_test = test["yield_kg"]

# Load trained model
model = joblib.load("models/linear_regression.joblib")

# Predictions
pred_test = model.predict(X_test)

# Residuals
residuals = y_test - pred_test

# Plot 1: Residuals vs Predicted
plt.figure(figsize=(6, 4))
plt.scatter(pred_test, residuals, alpha=0.5)
plt.axhline(0, color="red", linestyle="--")
plt.xlabel("Predicted Yield (kg)")
plt.ylabel("Residual (kg)")
plt.title("Residuals vs Predicted")
plt.tight_layout()
plt.savefig("reports/figures/residuals_linear.png", dpi=150)
plt.close()

# Plot 2: Residuals vs Humidity
humidity_col = [c for c in X_test.columns if "humidity" in c.lower()][0]

plt.figure(figsize=(6, 4))
plt.scatter(X_test[humidity_col], residuals, alpha=0.5)
plt.axhline(0, color="red", linestyle="--")
plt.xlabel("Scaled Humidity")
plt.ylabel("Residual (kg)")
plt.title("Residuals vs Humidity")
plt.tight_layout()
plt.savefig(
    "reports/figures/residuals_vs_humidity_linear.png",
    dpi=150
)
plt.close()

print("Diagnostic plots saved successfully.")