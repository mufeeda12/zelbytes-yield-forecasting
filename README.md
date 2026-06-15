# zelbytes-yield-forecasting

# Environment Setup

## Clone Repository

## Create Virtual Environment

### Windows

python -m venv venv

venv\Scripts\activate

### Linux/macOS

python3 -m venv venv

source venv/bin/activate

## Install Dependencies

pip install -r requirements.txt

## Run Smoke Test

python smoke_test.py

## Task 2

# 🌿 Polyhouse Yield Forecasting Pipeline

## 📌 Project Overview
This project implements a basic data pipeline for a polyhouse (controlled agricultural environment) sensor system. The goal is to support **yield forecasting** by processing environmental sensor data such as temperature, humidity, and CO₂ levels.

The pipeline covers:
- Data ingestion from raw sensor files
- Data validation and cleaning
- Handling missing values and duplicates
- Exporting cleaned data for analysis and modeling

---

## 📂 Project Structure
zelbytes-yield-forecasting/
│
├── data/
│ ├── raw/ # Original sensor data (CSV/XLSX)
│ ├── interim/ # Loaded dataset snapshot
│ └── processed/ # Cleaned dataset
│
├── src/
│ ├── ingest.py # Data ingestion script
│ └── clean.py # Data cleaning pipeline
│
├── cleaning_log.md # Data cleaning audit log
├── data_dictionary.md # Column definitions & units
├── .gitignore # Ignored files and folders
└── README.md


---

## 📊 Dataset Description

The dataset simulates real-time polyhouse sensor readings.

| Column | Description | Unit |
|--------|-------------|------|
| timestamp | Time of sensor reading | datetime |
| temperature_c | Air temperature inside polyhouse | °C |
| humidity_pct | Relative humidity | % |
| co2_ppm | CO₂ concentration | ppm |
| yield_kg | Crop yield (target variable) | kg |

📌 See `data_dictionary.md` for full details.

---

## ⚙️ Pipeline Workflow

### 1. Data Ingestion
- Reads raw sensor data (`CSV/XLSX`)
- Parses timestamp column
- Validates schema and data types
- Saves snapshot to:

---

### 2. Data Cleaning
- Handles missing values (sensor columns only)
- Applies forward-fill for short gaps
- Removes duplicate timestamps
- Filters invalid sensor readings:
  - humidity: 50–100%
  - temperature: 10–35°C
  - CO₂: 400–2000 ppm
- Drops rows with missing target (`yield_kg`)
- Saves cleaned dataset:


---

## 📌 Key Design Decisions

- **No imputation for target (`yield_kg`)** to avoid data leakage
- Median imputation used for sensor values
- Forward fill used for short sensor outages
- Duplicate timestamps removed to avoid bias in time-series analysis

---

## 📦 Dependencies

Install required packages:

```bash
pip install pandas pyarrow openpyxl

## Task 4: Train/Test Split & Data Leakage Prevention

### Chronological Split

The dataset was sorted by timestamp and split chronologically using an 80/20 ratio. The first 80% of records were used for training, while the remaining 20% were reserved for testing. This ensures that the model is trained on past observations and evaluated on future observations.

### Data Leakage Prevention

To prevent data leakage, the MinMaxScaler was fitted only on the training dataset using `fit_transform()`. The same scaler was then applied to the test dataset using `transform()`. This ensures that no statistical information from the test set influences the training process.

### Train and Test Sizes

Training set size: 80% of total records
Test set size: 20% of total records

The exact row counts were logged during execution.

### Feature Integrity

All features (`temperature_c`, `humidity_pct`, and `co2_ppm`) are derived from measurements recorded at the same timestamp. No feature uses information from future timestamps, ensuring realistic forecasting conditions.

### Saved Artifacts

The following artifacts were generated and saved for future modeling tasks:

* `data/processed/train.parquet`
* `data/processed/test.parquet`
* `models/minmax_scaler_train.joblib`

These files will be used in subsequent regression and forecasting experiments.
