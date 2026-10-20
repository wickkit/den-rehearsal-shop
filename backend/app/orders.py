"""Orders live in Postgres (DATABASE_URL); a checkout turns a cart into one."""
import os

import psycopg

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    cart_id TEXT NOT NULL,
    total NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
)
"""


def connect():
    conn = psycopg.connect(os.environ["DATABASE_URL"], autocommit=True)
    conn.execute(SCHEMA)
    return conn


def place(cart_id, total):
    with connect() as conn:
        row = conn.execute("INSERT INTO orders (cart_id, total) VALUES (%s, %s) RETURNING id",
                           (cart_id, total)).fetchone()
    return row[0]


def get(order_id):
    with connect() as conn:
        row = conn.execute("SELECT id, cart_id, total FROM orders WHERE id = %s", (order_id,)).fetchone()
    return None if row is None else {"id": row[0], "cart": row[1], "total": str(row[2])}


def count():
    with connect() as conn:
        return conn.execute("SELECT count(*) FROM orders").fetchone()[0]
