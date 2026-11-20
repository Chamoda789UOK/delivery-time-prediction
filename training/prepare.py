import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.read_csv("features.csv")

x = df.drop(columns=["Delivery_Time"])
y = df["Delivery_Time"]

x_train, x_temp, y_train, y_temp = train_test_split(x, y, test_size=0.30, random_state=42)
x_val, x_test, y_val, y_test = train_test_split(x_temp, y_temp, test_size=0.50, random_state=42)

number_cols = ["Agent_Age", "Agent_Rating", "distance_km", "order_hour", "day_of_week"]
text_cols = ["Weather", "Traffic", "Vehicle", "Area", "Category"]

prep = ColumnTransformer([
    ("num", StandardScaler(), number_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), text_cols),
])

x_train = prep.fit_transform(x_train)
x_val = prep.transform(x_val)
x_test = prep.transform(x_test)

print(x_train.shape, x_val.shape, x_test.shape)

joblib.dump(prep, "preprocessor.joblib")
np.savez("data.npz", x_train=x_train, x_val=x_val, x_test=x_test,
         y_train=y_train.values, y_val=y_val.values, y_test=y_test.values)