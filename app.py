import streamlit as st
import numpy as np
import pandas as pd
from src.predict import predict_yield
from pathlib import Path

MODEL_PATH = Path("models/random_forest_tuned.joblib")

if not MODEL_PATH.exists():
    st.error(
        "Model file not found.\nPlease train the model first."
    )
    st.stop()

st.set_page_config(
    page_title="Zelbytes Agritech | Mushroom Yield Forecast",
    page_icon="🍄",
    layout="centered"
)

# ---------------------------
# Cached predictor
# ---------------------------
@st.cache_resource
def load_predictor():
    return predict_yield

predict = load_predictor()

# ---------------------------
# Header
# ---------------------------
st.title("🍄 Zelbytes Agritech")
st.subheader("Polyhouse Mushroom Yield Forecast")

st.markdown("""
Estimate the expected **daily mushroom yield (kg/day)** using
polyhouse environmental sensor readings.

Adjust the sensor values from the sidebar and click **Predict Yield**.
""")

# ---------------------------
# Sidebar
# ---------------------------
with st.sidebar:

    st.header("Environmental Sensors")

    temp = st.slider(
        "Temperature (°C)",
        10.0,
        35.0,
        22.0,
        0.1
    )

    humidity = st.slider(
        "Humidity (%)",
        50.0,
        100.0,
        88.0,
        0.5
    )

    co2 = st.slider(
        "CO₂ (ppm)",
        400,
        2000,
        900,
        10
    )

    predict_btn = st.button("Predict Yield")

# ---------------------------
# Input validation
# ---------------------------
warnings = []

if not (15 <= temp <= 30):
    warnings.append("Temperature is outside the typical training range (15–30°C).")

if not (70 <= humidity <= 95):
    warnings.append("Humidity is outside the typical training range (70–95%).")

if not (500 <= co2 <= 1500):
    warnings.append("CO₂ is outside the typical training range (500–1500 ppm).")

for msg in warnings:
    st.warning(msg)

# ---------------------------
# Prediction
# ---------------------------
if predict_btn:

    with st.spinner("Generating prediction..."):
        prediction = predict(temp, humidity, co2)

    st.metric(
        "Estimated Daily Yield",
        f"{prediction:.2f} kg/day"
    )
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Estimated Yield",
            f"{prediction:.2f} kg/day"
        )

    with col2:
        st.metric(
            "Humidity",
            f"{humidity:.1f}%"
        )

    st.success("Prediction completed successfully.")

# ---------------------------
# Sensitivity Analysis
# ---------------------------
st.divider()

st.subheader("What-if Analysis")

st.markdown(
    "This chart shows how predicted yield changes when **humidity varies**, "
    "while **temperature (22°C)** and **CO₂ (900 ppm)** remain constant."
)

temp_fixed = 22.0
co2_fixed = 900

humid_range = np.linspace(70, 98, 29)

preds = [
    predict(temp_fixed, h, co2_fixed)
    for h in humid_range
]

chart_df = pd.DataFrame({
    "Humidity (%)": humid_range,
    "Predicted Yield (kg/day)": preds
})

st.line_chart(
    chart_df,
    x="Humidity (%)",
    y="Predicted Yield (kg/day)"
)

# ---------------------------
# Model Information
# ---------------------------
with st.expander("📋 Model Information"):

    st.markdown("""
**Model Version:** v1.0

**Algorithm:** Tuned Random Forest

**Last Training Date:** Replace with your actual date

**Test MAE:** Replace with your actual MAE

**Prediction Unit:** Kilograms per day (kg/day)

**Training Dataset:** Polyhouse environmental sensor readings

**Inputs Used**
- Temperature (°C)
- Humidity (%)
- CO₂ (ppm)
""")

# ---------------------------
# Methodology
# ---------------------------
st.divider()

st.markdown("### 📖 Methodology")

st.markdown(
    "See the project methodology in the **README.md** or **reports/methodology.md**."
)

st.caption("Developed by Zelbytes Agritech")