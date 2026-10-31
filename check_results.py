import pandas as pd
from services.sales import get_kpis

df = pd.read_csv("data/clean_orders.csv")
valid = df[~df["status"].str.startswith("Cancelled", na=False)]

print("pandas revenue: ", round(valid["amount"].sum(), 2))
print("pandas orders : ", valid["order_id"].nunique())
print()
print("SQL results:")
print(get_kpis())