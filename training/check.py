import pandas as pd

df = pd.read_csv("amazon_delivery.csv")

for col in ["Weather", "Traffic", "Vehicle", "Area", "Category"]:
    df[col] = df[col].str.strip()

df["Traffic"] = df["Traffic"].mask(df["Traffic"] == "NaN")

print(df["Traffic"].isnull().sum())
print((df["Agent_Rating"] > 5).sum())
print((df["Store_Latitude"] < 1).sum(), (df["Store_Longitude"] < 1).sum())
print((df["Drop_Latitude"] < 1).sum(), (df["Drop_Longitude"] < 1).sum())