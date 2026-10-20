"""GET /orders/count reads Postgres; checkouts in another land's database must not show up here."""
import time

from fastapi.testclient import TestClient

from app import orders
from app.main import CARTS, app

client = TestClient(app)


def setup_function():
    CARTS.clear()
    with orders.connect() as conn:
        conn.execute("TRUNCATE orders RESTART IDENTITY")


def test_order_count_follows_checkouts():
    assert client.get("/orders/count").json() == {"orders": 0}
    for i in range(4):
        client.post(f"/carts/n{i}/lines", json={"item": "spoon"})
        client.post(f"/carts/n{i}/checkout")
        time.sleep(0.3)
    assert client.get("/orders/count").json() == {"orders": 4}
