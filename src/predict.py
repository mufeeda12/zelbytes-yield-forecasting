import csv
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd

# ----------------------------
# Logging Configuration
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent   # src/
PROJECT_DIR = BASE_DIR.parent               # root

LOG_PATH = PROJECT_DIR / "logs" / "predictions.csv"


def log_prediction(temp, humid, co2, predicted_kg):
    """Log every prediction to a CSV file."""

    LOG_PATH.parent.mkdir(exist_ok=True)

    write_header = not LOG_PATH.exists()

    with LOG_PATH.open("a", newline="") as f:
        writer = csv.writer(f)

        if write_header:
            writer.writerow([
                "timestamp_utc",
                "temp_c",
                "humidity_pct",
                "co2_ppm",
                "predicted_kg"
            ])

        writer.writerow([
            datetime.now(timezone.utc).isoformat(),
            temp,
            humid,
            co2,
            round(predicted_kg, 3)
        ])


# ----------------------------
# Load Model and Scaler
# ----------------------------
MODEL_DIR = Path("models")

_scaler = joblib.load(MODEL_DIR / "minmax_scaler_train.joblib")
_model = joblib.load(MODEL_DIR / "random_forest_tuned.joblib")

# Feature names used during training
_feature_cols = [
    "temperature_scaled",
    "humidity_scaled",
    "CO2_scaled"
]


# ----------------------------
# Prediction Function
# ----------------------------
def predict_yield(
    temperature: float,
    humidity: float,
    CO2: float
) -> float:
    """
    Predict mushroom yield based on
    temperature, humidity and CO₂.
    """

    # Raw input dataframe
    raw = pd.DataFrame(
        [[temperature, humidity, CO2]],
        columns=[
            "temperature",
            "humidity",
            "CO2"
        ]
    )

    # Scale inputs
    scaled_array = _scaler.transform(raw)

    scaled = pd.DataFrame(
        scaled_array,
        columns=_feature_cols
    )

    # Predict
    prediction = float(_model.predict(scaled)[0])

    # Log prediction
    log_prediction(
        temperature,
        humidity,
        CO2,
        prediction
    )

    return prediction


def make_prediction(
    temperature: float,
    humidity: float,
    CO2: float
) -> float:
    return predict_yield(
        temperature,
        humidity,
        CO2
    )


# ----------------------------
# Command Line Test
# ----------------------------
if __name__ == "__main__":

    pred = make_prediction(
        temperature=25.0,
        humidity=80.0,
        CO2=920
    )

    print(f"Predicted Yield: {pred:.2f} kg")