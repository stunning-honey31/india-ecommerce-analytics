import pandas as pd

df = pd.read_csv("data/raw/Amazon Sale Report.csv", low_memory=False)
df.columns = (df.columns.str.strip().str.lower().str.replace(r'[^a-z0-9]+', '_', regex=True))
print(df.columns.tolist())

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.drop_duplicates()
print(df["date"].head()) 

df["ship_state"] = df["ship_state"].str.strip().str.title()
print(df["ship_state"].value_counts())

df.to_csv("data/clean_orders.csv", index=False)
print("Saved", df.shape)