"""
Feature Definitions

temperature
    Polyhouse temperature in degrees Celsius.

humidity
    Relative humidity percentage.

CO2
    Carbon dioxide concentration in parts per million.

temp_humid_interaction
    Formula:
        temperature × humidity / 100

    Purpose:
        Captures the combined effect of temperature and humidity
        on mushroom growth.

Target

yield
    Mushroom yield in kilograms.
"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib

df = pd.read_parquet("data/interim/02_cleaned.parquet").sort_values("timestamp")

df["temp_humid_interaction"] = df["temperature"] * df["humidity"] / 100

feature_cols = ["temperature", "humidity", "CO2", "temp_humid_interaction"]
X = df[feature_cols]
y = df["yield"]

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

joblib.dump(scaler, "models/minmax_scaler.joblib")

processed = pd.DataFrame(X_scaled, columns=[c + "_scaled" for c in feature_cols])
processed["yield"] = y.values
processed.to_parquet("data/processed/features.parquet", index=False)