import json
import pandas as pd
import joblib
from pathlib import Path

MODEL_DIR = Path("models")

_scaler = joblib.load(MODEL_DIR / "minmax_scaler_train.joblib")
_model = joblib.load(MODEL_DIR / "random_forest_tuned.joblib")

# IMPORTANT: these must be SCALED feature names
_feature_cols = [
    "temperature_scaled",
    "humidity_scaled",
    "CO2_scaled"
]


def predict_yield(
    temperature: float,
    humidity: float,
    CO2: float
) -> float:

    # 1. raw input
    raw = pd.DataFrame(
        [[temperature, humidity, CO2]],
        columns=["temperature", "humidity", "CO2"]
    )

    # 2. scale (numpy output)
    scaled_array = _scaler.transform(raw)

    # 3. rebuild with CORRECT training column names
    scaled = pd.DataFrame(
        scaled_array,
        columns=_feature_cols
    )

    # 4. predict
    prediction = _model.predict(scaled)[0]

    return float(prediction)


def make_prediction(temperature: float, humidity: float, CO2: float) -> float:
    return predict_yield(temperature, humidity, CO2)


if __name__ == "__main__":
    pred = make_prediction(
        temperature=25.0,
        humidity=80.0,
        CO2=920
    )

    print(f"Predicted Yield: {pred:.2f} kg")
