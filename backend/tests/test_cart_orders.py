"""GET /carts/{id}/orders lists that cart's orders from Postgres, oldest first."""
import time

from fastapi.testclient import TestClient

from app import orders
from app.main import CARTS, app

client = TestClient(app)


def setup_function():
    CARTS.clear()
    with orders.connect() as conn:
        conn.execute("TRUNCATE orders RESTART IDENTITY")


def test_a_carts_orders_are_listed():
    for item in ("tea", "mug", "tea"):
        client.post("/carts/r/lines", json={"item": item})
        client.post("/carts/r/checkout")
        time.sleep(0.3)
    client.post("/carts/other/lines", json={"item": "spoon"})
    client.post("/carts/other/checkout")
    got = client.get("/carts/r/orders").json()
    assert [o["total"] for o in got] == ["4.20", "9.99", "4.20"]
    assert [o["id"] for o in got] == [1, 2, 3]
    assert client.get("/carts/nobody/orders").json() == []
