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


task 7

# GridSearchCV Tuning Summary

## Objective

The objective was to improve Random Forest performance by tuning key hyperparameters using GridSearchCV.

## Parameter Grid

* n_estimators: [50, 100, 200]

  * Controls the number of trees in the forest.
  * More trees can improve performance but increase runtime.

* max_depth: [None, 8, 16]

  * Controls tree depth.
  * Shallower trees may reduce overfitting.

* min_samples_leaf: [1, 3, 5]

  * Controls the minimum number of samples required in a leaf node.
  * Larger values can improve generalization.

## Methodology

GridSearchCV was performed using TimeSeriesSplit with 3 folds. Only the training dataset was used during tuning. Mean Absolute Error (MAE) was used as the scoring metric.

## Results

* Best parameters: See `models/rf_best_params.json`
* Best model: `models/random_forest_tuned.joblib`
* CV results: `reports/gridsearch_results.csv`

The tuned model was evaluated once on the held-out test set after tuning.

## Runtime

The total GridSearch runtime was recorded in `reports/gridsearch_metrics.json`.

## Conclusion

GridSearchCV identified the best combination of hyperparameters for the Random Forest model while avoiding data leakage. The tuned model will be used for final model comparison and selection.

phase 2 (day 15 last)

🌱 Yield Forecasting using Machine Learning

This project predicts crop yield based on environmental parameters such as temperature, humidity, and CO2 levels using a trained Machine Learning model.

📁 Project Structure

zelbytes-yield-forecasting/
│
├── data/
├── models/
│ ├── minmax_scaler_train.joblib
│ ├── random_forest_tuned.joblib
│ └── feature_cols.json
│
├── src/
│ └── predict.py
│
├── requirements.txt
└── README.md

⚙️ Requirements

Install dependencies using:

pip install -r requirements.txt

🚀 How to Run Prediction

Run the script using:

python src/predict.py

📌 Example Output

Input: T=25, H=90, CO2=1000 → Predicted Yield: 1.16 kg

🧠 Model Details
Algorithm: Random Forest Regressor
Scaling: MinMaxScaler
Input Features:
temperature
humidity
CO2
Target: yield_kg
🔄 Workflow
Data collection and cleaning
Feature scaling using MinMaxScaler
Model training using Random Forest
Model saving using joblib
Inference using saved scaler + model
📊 Python Usage Example

from src.predict import make_prediction

result = make_prediction(25, 90, 1000)
print(result)

📦 Requirements
pandas
numpy
scikit-learn
joblib