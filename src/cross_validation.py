import pandas as pd
from pathlib import Path
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

# Load training data
train = pd.read_parquet("data/processed/train.parquet")

X_train = train.drop(columns=["yield_kg"])
y_train = train["yield_kg"]

# Time-series cross validation
tscv = TimeSeriesSplit(n_splits=5)

# Models
rf = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

lin = LinearRegression()

# Cross-validation MAE
rf_scores = -cross_val_score(
    rf,
    X_train,
    y_train,
    cv=tscv,
    scoring="neg_mean_absolute_error"
)

lin_scores = -cross_val_score(
    lin,
    X_train,
    y_train,
    cv=tscv,
    scoring="neg_mean_absolute_error"
)

rf_cv_mean = rf_scores.mean()
rf_cv_std = rf_scores.std()

lin_cv_mean = lin_scores.mean()
lin_cv_std = lin_scores.std()

print("Random Forest CV MAE:", rf_cv_mean, "+/-", rf_cv_std)
print("Linear Regression CV MAE:", lin_cv_mean, "+/-", lin_cv_std)

# Previous metrics from earlier tasks
linear_train_mae = 0.0780
linear_test_mae = 0.0838

Path("reports").mkdir(exist_ok=True)

with open("reports/cv_results.md", "w") as f:
    f.write("# Cross Validation Results\n\n")

    f.write("## Method\n")
    f.write(
        "TimeSeriesSplit with 5 folds was used to preserve "
        "chronological order and prevent data leakage.\n\n"
    )

    f.write("## Linear Regression\n")
    f.write(f"- Fold MAE: {lin_scores.tolist()}\n")
    f.write(f"- Average CV MAE: {lin_cv_mean:.4f}\n")
    f.write(f"- Standard Deviation: {lin_cv_std:.4f}\n\n")

    f.write("## Random Forest\n")
    f.write(f"- Fold MAE: {rf_scores.tolist()}\n")
    f.write(f"- Average CV MAE: {rf_cv_mean:.4f}\n")
    f.write(f"- Standard Deviation: {rf_cv_std:.4f}\n\n")

    f.write("## Overfitting Analysis\n")
    f.write(
        f"Linear Regression train MAE = {linear_train_mae:.4f}, "
        f"test MAE = {linear_test_mae:.4f}. "
        "The small difference suggests limited overfitting and "
        "good generalization.\n\n"
    )

    f.write("## Variance Interpretation\n")
    f.write(
        "A low standard deviation indicates stable model "
        "performance across folds. A high standard deviation "
        "suggests the model performance varies between time periods.\n\n"
    )

    f.write("## Conclusion\n")
    if rf_cv_mean < lin_cv_mean:
        f.write(
            "Random Forest achieved a lower average CV MAE and "
            "therefore performed better during cross-validation."
        )
    else:
        f.write(
            "Linear Regression achieved a lower average CV MAE and "
            "therefore performed better during cross-validation."
        )

print("CV report saved to reports/cv_results.md")