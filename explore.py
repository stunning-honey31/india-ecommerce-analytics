import pandas as pd

df = pd.read_csv("data/raw/Amazon Sale Report.csv", low_memory=False)
print(df.shape)
print(df.columns.tolist())
print(df.head())
print(df.isna().sum())
print(df["Status"].value_counts())
print("Duplicates:", df.duplicated().sum())