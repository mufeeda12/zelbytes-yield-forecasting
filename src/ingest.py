# src/ingest.py
import pandas as pd
from pathlib import Path

RAW = Path("data/raw/polyhouse sensors v2.csv")
INTERIM = Path("data/interim")
INTERIM.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(
    RAW,
    parse_dates=["timestamp"],
    dtype={
        "temperature": "float64",
        "humidity": "float64",
        "CO2": "float64",
        "yield": "float64",
    },
)

print(df.shape)
print(df.dtypes)
print(df.head())

df.to_parquet(INTERIM / "01_loaded.parquet", index=False)
