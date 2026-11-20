import joblib
import pandas as pd
from tensorflow import keras

model = keras.models.load_model("best_model.keras")
prep = joblib.load("preprocessor.joblib")

base = {
    "Agent_Age": 30,
    "Agent_Rating": 4.7,
    "Weather": "Sunny",
    "Traffic": "Low",
    "Vehicle": "motorcycle",
    "Area": "Urban",
    "Category": "Electronics",
    "distance_km": 8.0,
    "order_hour": 14,
    "day_of_week": 2,
}

cases = {
    "normal": base,
    "heavy traffic": {**base, "Traffic": "Jam"},
    "long distance": {**base, "distance_km": 20.0},
}

for name, case in cases.items():
    result = model.predict(prep.transform(pd.DataFrame([case])), verbose=0)[0][0]
    print(name, "->", round(float(result), 1), "minutes")