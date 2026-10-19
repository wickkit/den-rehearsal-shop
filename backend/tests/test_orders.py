"""Checkout writes to Postgres. These need DATABASE_URL (CI starts a postgres service)."""
import time

from fastapi.testclient import TestClient

from app import orders
from app.main import CARTS, app

client = TestClient(app)


def setup_function():
    CARTS.clear()
    with orders.connect() as conn:
        conn.execute("TRUNCATE orders RESTART IDENTITY")


def test_checkout_stores_an_order():
    client.post("/carts/a/lines", json={"item": "tea", "qty": 2})
    o = client.post("/carts/a/checkout").json()
    assert o == {"id": 1, "cart": "a", "total": "8.40"}
    assert client.get("/orders/1").json() == o
    assert "a" not in CARTS


def test_orders_are_counted_exactly():
    # A database shared with another run would add its orders in between.
    for i in range(5):
        client.post(f"/carts/c{i}/lines", json={"item": "mug"})
        client.post(f"/carts/c{i}/checkout")
        time.sleep(0.2)
    assert orders.count() == 5


def test_unknown_order_is_404():
    assert client.get("/orders/999").status_code == 404
