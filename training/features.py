import numpy as np
import pandas as pd

df = pd.read_csv("clean_data.csv")

lat1 = np.radians(df["Store_Latitude"])
lon1 = np.radians(df["Store_Longitude"])
lat2 = np.radians(df["Drop_Latitude"])
lon2 = np.radians(df["Drop_Longitude"])

a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
df["distance_km"] = 6371 * 2 * np.arcsin(np.sqrt(a))

df["order_hour"] = pd.to_datetime(df["Order_Time"], format="%H:%M:%S").dt.hour
df["day_of_week"] = pd.to_datetime(df["Order_Date"]).dt.dayofweek

df = df.drop(columns=[
    "Order_ID", "Pickup_Time", "Order_Date", "Order_Time",
    "Store_Latitude", "Store_Longitude", "Drop_Latitude", "Drop_Longitude",
])

print(df.shape)
print(df.head())
print(df["distance_km"].describe())
df.to_csv("features.csv", index=False)