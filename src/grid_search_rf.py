import pandas as pd
import json
import joblib
import time
from pathlib import Path

from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load data
train = pd.read_parquet("data/processed/train.parquet")
test = pd.read_parquet("data/processed/test.parquet")

X_train = train.drop(columns=["yield_kg"])
y_train = train["yield_kg"]

X_test = test.drop(columns=["yield_kg"])
y_test = test["yield_kg"]

# Time-series cross-validation
tscv = TimeSeriesSplit(n_splits=3)

# Parameter grid
param_grid = {
    "n_estimators": [50, 100, 200],
    "max_depth": [None, 8, 16],
    "min_samples_leaf": [1, 3, 5],
}

rf = RandomForestRegressor(
    random_state=42,
    n_jobs=-1
)

start_time = time.time()

search = GridSearchCV(
    estimator=rf,
    param_grid=param_grid,
    cv=tscv,
    scoring="neg_mean_absolute_error",
    n_jobs=-1,
    refit=True,
)

search.fit(X_train, y_train)

runtime = time.time() - start_time

print("Best Parameters:", search.best_params_)
print("Best CV MAE:", -search.best_score_)

best_model = search.best_estimator_

# Evaluate on test set ONCE
pred = best_model.predict(X_test)

mae = mean_absolute_error(y_test, pred)
rmse = mean_squared_error(y_test, pred) ** 0.5
r2 = r2_score(y_test, pred)

print("Test MAE:", mae)
print("Test RMSE:", rmse)
print("Test R2:", r2)

# Create folders
Path("models").mkdir(exist_ok=True)
Path("reports").mkdir(exist_ok=True)

# Save best model
joblib.dump(
    best_model,
    "models/random_forest_tuned.joblib"
)

# Save best parameters
with open("models/rf_best_params.json", "w") as f:
    json.dump(search.best_params_, f, indent=4)

# Save CV results
cv_results = pd.DataFrame(search.cv_results_)
cv_results.head(20).to_csv(
    "reports/gridsearch_results.csv",
    index=False
)

# Save metrics
with open("reports/gridsearch_metrics.json", "w") as f:
    json.dump(
        {
            "best_cv_mae": float(-search.best_score_),
            "test_mae": float(mae),
            "test_rmse": float(rmse),
            "test_r2": float(r2),
            "runtime_seconds": round(runtime, 2)
        },
        f,
        indent=4
    )

print(f"Runtime: {runtime:.2f} seconds")