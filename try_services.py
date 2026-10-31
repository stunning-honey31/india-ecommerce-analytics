from services.sales import (
    get_revenue_by_month, get_top_categories, get_kpis,
    get_order_by_state, get_cancellation_by_fulfilment, get_order_by_id
)

print(get_kpis())
print(get_order_by_state().head(10))
print(get_cancellation_by_fulfilment())
print(get_top_categories())
print(get_revenue_by_month().head())

from services.db import get_connection
conn = get_connection()
real_id = conn.execute("SELECT order_id FROM orders LIMIT 1").fetchone()[0]
conn.close()
print(get_order_by_id(real_id))