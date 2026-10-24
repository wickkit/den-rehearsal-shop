"""A tiny shop API: a catalogue, a cart, and a checkout total."""
from decimal import ROUND_HALF_UP, Decimal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Rehearsal Shop")

CATALOGUE = {
    "tea": {"name": "Green tea", "price": Decimal("4.20")},
    "mug": {"name": "Blue mug", "price": Decimal("9.99")},
    "spoon": {"name": "Brass spoon", "price": Decimal("2.15")},
}

CARTS: dict[str, dict[str, int]] = {}


class Line(BaseModel):
    item: str
    qty: int = 1


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/orders/count")
def order_count():
    from app import orders
    return {"orders": orders.count()}


@app.get("/items")
@app.get("/products")
def items(sort: str | None = None):
    rows = list(CATALOGUE.items())
    if sort == "price":
        rows.sort(key=lambda kv: kv[1]["price"])
    elif sort is not None:
        raise HTTPException(422, "sort must be 'price'")
    return [{"id": k, "name": v["name"], "price": str(v["price"])} for k, v in rows]


@app.get("/items/{item_id}")
def item(item_id: str):
    if item_id not in CATALOGUE:
        raise HTTPException(404, "no such item")
    v = CATALOGUE[item_id]
    return {"id": item_id, "name": v["name"], "price": str(v["price"])}


@app.post("/carts/{cart_id}/lines")
def add_line(cart_id: str, line: Line):
    if line.item not in CATALOGUE:
        raise HTTPException(404, "no such item")
    if line.qty < 1:
        raise HTTPException(422, "qty must be at least 1")
    cart = CARTS.setdefault(cart_id, {})
    cart[line.item] = cart.get(line.item, 0) + line.qty
    return {"cart": cart_id, "lines": cart}


def total(lines: dict[str, int], discount_pct: int = 0) -> Decimal:
    subtotal = sum(CATALOGUE[k]["price"] * q for k, q in lines.items())
    off = subtotal * Decimal(discount_pct) / 100
    off = off.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return (subtotal - off).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


@app.get("/carts/{cart_id}/total")
def cart_total(cart_id: str, discount: int = 0):
    if cart_id not in CARTS:
        raise HTTPException(404, "no such cart")
    return {"cart": cart_id, "total": str(total(CARTS[cart_id], discount))}


@app.post("/carts/{cart_id}/checkout")
def checkout(cart_id: str, discount: int = 0):
    from app import orders
    if cart_id not in CARTS:
        raise HTTPException(404, "no such cart")
    order_id = orders.place(cart_id, total(CARTS.pop(cart_id), discount))
    return orders.get(order_id)


@app.get("/orders/{order_id}")
def order(order_id: int):
    from app import orders
    if (o := orders.get(order_id)) is None:
        raise HTTPException(404, "no such order")
    return o


@app.get("/carts/{cart_id}/orders")
def cart_orders(cart_id: str):
    from app import orders
    return orders.for_cart(cart_id)
