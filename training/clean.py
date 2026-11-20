import pandas as pd

df = pd.read_csv("amazon_delivery.csv")

for col in ["Weather", "Traffic", "Vehicle", "Area", "Category"]:
    df[col] = df[col].str.strip()

df["Traffic"] = df["Traffic"].mask(df["Traffic"] == "NaN")
df = df.dropna()

df = df[df["Agent_Rating"] <= 5]

for col in ["Store_Latitude", "Drop_Latitude"]:
    df = df[df[col].between(6, 38)]
for col in ["Store_Longitude", "Drop_Longitude"]:
    df = df[df[col].between(68, 98)]

df = df[~df["Vehicle"].eq("bicycle")]

print(df.shape)
df.to_csv("clean_data.csv", index=False)