import pandas as pd
from services.db import get_connection

def get_revenue_by_month(state=None):
    query = """
        SELECT strftime('%Y-%m', o.order_date) AS month,
               SUM(oi.amount) AS revenue
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.status NOT LIKE 'Cancelled%'
            AND (? IS NULL OR o.ship_state = ?)
        GROUP BY month
        ORDER BY month
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn, params=(state, state))
    conn.close()
    return df

def get_top_categories(limit=10):
    query = """
        SELECT p.category, SUM(oi.amount) AS revenue
        FROM order_items oi
        JOIN products p ON oi.sku = p.sku
        GROUP BY p.category
        ORDER BY revenue DESC
        LIMIT ?
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn, params=(limit,))
    conn.close()
    return df

def get_kpis():
    query = """
        SELECT COUNT(DISTINCT o.order_id) AS total_orders,
               ROUND(SUM(oi.amount), 2) AS total_revenue,
               ROUND(SUM(oi.amount) * 1.0 / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.status NOT LIKE 'Cancelled%'
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_order_by_state():
    query = """
        SELECT o.ship_state,
                COUNT(DISTINCT o.order_id) AS orders,
                ROUND(SUM(oi.amount), 2) AS revenue
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.status NOT LIKE 'Cancelled%'
        GROUP BY o.ship_state
        ORDER BY revenue DESC
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
