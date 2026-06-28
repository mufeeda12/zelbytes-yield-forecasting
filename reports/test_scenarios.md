| Scenario | Temp | Humidity | CO₂  | Expected Behaviour |
| -------- | ---- | -------- | ---- | ------------------ |
| Normal   | 22   | 88       | 900  | Normal prediction  |
| Dry      | 22   | 70       | 900  | Lower yield        |
| Heat     | 32   | 88       | 900  | Warning shown      |
| High CO₂ | 22   | 88       | 1800 | Warning shown      |
| Cold     | 14   | 90       | 900  | Warning shown      |
