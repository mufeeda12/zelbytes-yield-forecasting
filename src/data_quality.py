import pandas as pd
from pathlib import Path
df = pd.read_parquet("data/interim/02_cleaned.parquet")

summary = df[["temperature", "humidity", "CO2", "yield"]].describe().T
summary["cv"] = summary["std"] / summary["mean"]

report = []
report.append(f"# Polyhouse Data Quality Report\n")
report.append(f"Rows: {len(df)}\n")
report.append(f"Date range: {df['timestamp'].min()} → {df['timestamp'].max()}\n\n")
report.append(summary.to_markdown())

Path("reports").mkdir(exist_ok=True)
Path("reports/data_quality.md").write_text("\n".join(report), encoding="utf-8")