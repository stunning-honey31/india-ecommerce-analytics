CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    order_date DATE,
    status TEXT,
    fulfilment TEXT,
    sales_channel TEXT,
    is_b2b INTEGER,
    ship_city TEXT,
    ship_state TEXT,
    ship_postal_code TEXT
);

CREATE TABLE products (
    sku TEXT PRIMARY KEY,
    category TEXT,
    size TEXT
);

CREATE TABLE order_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT REFERENCES orders(order_id),
    sku TEXT REFERENCES products(sku),
    qty INTEGER,
    amount REAL
);

CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_state ON orders(ship_state);