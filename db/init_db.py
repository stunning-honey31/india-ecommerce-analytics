import os
import sqlite3
import pandas as pd

df = pd.read_csv("data/clean_orders.csv")
df["sku"] = (
    df["category"].fillna("Unknown").str.strip() + "-" +
    df["size"].fillna("NA").astype(str).str.strip()
)

if os.path.exists("db/shop.db"):
    os.remove("db/shop.db")          # start fresh each time

conn = sqlite3.connect("db/shop.db")
conn.executescript(open("db/schema.sql").read())

orders = df[["order_id", "date", "status", "fulfilment", "sales_channel",
            "b2b", "ship_city", "ship_state", "ship_postal_code"]]
orders = orders.drop_duplicates("order_id")
orders.columns = ["order_id", "order_date", "status", "fulfilment",
                    "sales_channel", "is_b2b", "ship_city", "ship_state",
                    "ship_postal_code"]

products = df[["sku", "category", "size"]].drop_duplicates("sku")
items = df[["order_id", "sku", "qty", "amount"]]

orders.to_sql("orders", conn, if_exists="append", index=False)
products.to_sql("products", conn, if_exists="append", index=False)
items.to_sql("order_items", conn, if_exists="append", index=False)

conn.commit()
for t in ["orders", "products", "order_items"]:
    print(t, conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0])
conn.close()
print("Database built")