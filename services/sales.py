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

def get_cancellation_by_fulfilment():
    query = """
        SELECT fulfilment,
               COUNT(*) AS total_orders,
               SUM(CASE WHEN status LIKE 'Cancelled%' THEN 1 ELSE 0 END) AS cancelled,
               ROUND(100.0 * SUM(CASE WHEN status LIKE 'Cancelled%' THEN 1 ELSE 0 END)
                     / COUNT(*), 2) AS cancel_rate_pct
        FROM orders
        GROUP BY fulfilment
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def get_order_by_id(order_id):
    query = """
        SELECT o.order_id, o.order_date, o.status, o.ship_city, o.ship_state,
               p.category, p.size, oi.qty, oi.amount
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.sku = p.sku
        WHERE o.order_id = ?
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn, params=(order_id,))
    conn.close()
    return df
