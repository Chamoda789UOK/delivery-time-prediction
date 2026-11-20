import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("amazon_delivery.csv")

print(df.describe())
print(df.isnull().sum())
print("duplicates:", df.duplicated().sum())

for col in ["Weather", "Traffic", "Vehicle", "Area", "Category"]:
    print(df[col].value_counts())

df["Delivery_Time"].hist(bins=40)
plt.xlabel("Delivery time (minutes)")
plt.ylabel("Count")
plt.show()