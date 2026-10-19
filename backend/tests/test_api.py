from decimal import Decimal

from fastapi.testclient import TestClient

from app.main import CARTS, app, total

client = TestClient(app)


def setup_function():
    CARTS.clear()


def test_health():
    assert client.get("/health").json() == {"ok": True}


def test_items_lists_catalogue():
    ids = [i["id"] for i in client.get("/items").json()]
    assert ids == ["tea", "mug", "spoon"]


def test_add_line_and_total():
    client.post("/carts/a/lines", json={"item": "tea", "qty": 2})
    client.post("/carts/a/lines", json={"item": "mug"})
    assert client.get("/carts/a/total").json()["total"] == "18.39"


def test_unknown_item_is_404():
    assert client.post("/carts/a/lines", json={"item": "kettle"}).status_code == 404


def test_zero_qty_is_rejected():
    assert client.post("/carts/a/lines", json={"item": "tea", "qty": 0}).status_code == 422


def test_unknown_cart_total_is_404():
    assert client.get("/carts/nope/total").status_code == 404


def test_discount_rounds_half_up():
    # Red on purpose until issue #1 is fixed: 10% of 2.15 is 0.215, which
    # rounds to 0.22 off, so the total is 1.93.
    assert total({"spoon": 1}, discount_pct=10) == Decimal("1.93")
