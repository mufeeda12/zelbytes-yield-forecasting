import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib

# Load and sort data
df = (
    pd.read_parquet("data/interim/02_cleaned.parquet")
    .sort_values("timestamp")
    .reset_index(drop=True)
)

feature_cols = ["temperature", "humidity", "CO2"]

# Chronological 80/20 split
split_idx = int(len(df) * 0.8)
train, test = df.iloc[:split_idx], df.iloc[split_idx:]

# Scale features
scaler = MinMaxScaler()

X_train = scaler.fit_transform(train[feature_cols])
X_test = scaler.transform(test[feature_cols])

y_train = train["yield"].values
y_test = test["yield"].values

# Save scaler
joblib.dump(scaler, "models/minmax_scaler_train.joblib")

# Save processed train set
pd.DataFrame(
    X_train,
    columns=[c + "_scaled" for c in feature_cols]
).assign(yield_kg=y_train).to_parquet(
    "data/processed/train.parquet",
    index=False
)

# Save processed test set
pd.DataFrame(
    X_test,
    columns=[c + "_scaled" for c in feature_cols]
).assign(yield_kg=y_test).to_parquet(
    "data/processed/test.parquet",
    index=False
)

# Summary
print(f"Train: {train['timestamp'].min()} → {train['timestamp'].max()}")
print(f"Test:  {test['timestamp'].min()} → {test['timestamp'].max()}")

print("Train rows:", len(train))
print("Test rows:", len(test))