# Data Cleaning Log

Dataset: Polyhouse Sensor Dataset

## Missing Value Handling

* Checked missing values in all columns.
* Applied forward-fill (limit=2) to sensor columns:

  * temperature_c
  * humidity_pct
  * co2_ppm
* Did not impute yield_kg to avoid target leakage.
* Rows with missing yield_kg were removed.

## Validity Rules

* Humidity: 50–100%
* Temperature: 10–35°C
* CO₂: 400–2000 ppm

Rows violating these rules were removed from the dataset.

## Duplicate Handling

* Removed duplicate timestamps using the latest observation (`keep="last"`).

## Output

Cleaned dataset saved as:

data/interim/02_cleaned.parquet
