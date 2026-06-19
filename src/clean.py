import pandas as pd
from pathlib import Path

df = pd.read_parquet("data/interim/01_loaded.parquet")

# Missing report
print(df.isna().sum())

# Valid ranges for oyster polyhouse
valid = (
    df["humidity"].between(50, 100)
    & df["temperature"].between(10, 35)
    & df["CO2"].between(400, 2000)
    & df["yield"].notna()
)
df = df[valid].copy()

# Short gap: forward-fill sensor columns only
cols = ["temperature", "humidity", "CO2"]
df[cols] = df[cols].ffill(limit=2)

# Drop remaining rows with null target
df = df.dropna(subset=["yield"])

# Duplicates by timestamp
df = df.drop_duplicates(subset=["timestamp"], keep="last")

df.to_parquet("data/interim/02_cleaned.parquet", index=False)
print(f"Clean rows: {len(df)}")