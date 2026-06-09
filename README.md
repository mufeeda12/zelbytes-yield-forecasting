# zelbytes-yield-forecasting

# Environment Setup

## Clone Repository

git clone https://github.com/<your-username>/zelbytes-yield-forecasting.git

cd zelbytes-yield-forecasting

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