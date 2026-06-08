import pandas as pd

sample_raw = {
    "temprature":24.7,
    "humidity":87,
    "co2":950,
    "yield":18.2
}

df = pd.DataFrame([sample_raw])

print("sample polyhouse sensor data")
print(df)