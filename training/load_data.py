import pandas as pd

df = pd.read_csv("amazon_delivery.csv")
print(df.shape)
print(df.head())
print(df.info())