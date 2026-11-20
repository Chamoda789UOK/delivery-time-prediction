import json
from datetime import date

import joblib
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from tensorflow import keras

data = np.load("data.npz")
x_test, y_test = data["x_test"], data["y_test"]

model = keras.models.load_model("best_model.keras")
prep = joblib.load("preprocessor.joblib")
pred = model.predict(x_test).flatten()

mse = mean_squared_error(y_test, pred)

info = {
    "model_version": "1.0.0",
    "training_date": str(date.today()),
    "dataset": "Amazon Delivery Dataset (Kaggle), 39958 rows after cleaning",
    "target": "Delivery_Time (minutes)",
    "features": list(prep.feature_names_in_),
    "architecture": "Dense 128-64-32 ReLU, 1 linear output, Adam lr 0.001, MSE loss",
    "metrics": {
        "mae": round(float(mean_absolute_error(y_test, pred)), 2),
        "rmse": round(float(np.sqrt(mse)), 2),
        "r2": round(float(r2_score(y_test, pred)), 3),
    },
}

with open("model_info.json", "w") as f:
    json.dump(info, f, indent=2)

print(json.dumps(info, indent=2))