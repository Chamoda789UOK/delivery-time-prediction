import json
from pathlib import Path

import joblib
import pandas as pd
from tensorflow import keras

folder = Path(__file__).parent

model = keras.models.load_model(folder / "best_model.keras")
prep = joblib.load(folder / "preprocessor.joblib")
info = json.loads((folder / "model_info.json").read_text())


def predict_minutes(delivery):
    frame = pd.DataFrame([delivery])
    result = model.predict(prep.transform(frame), verbose=0)[0][0]
    return max(0.0, round(float(result), 1))