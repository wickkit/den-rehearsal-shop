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


@app.get("/items")
def items():
    return [{"id": k, "name": v["name"], "price": str(v["price"])} for k, v in CATALOGUE.items()]


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
    # Known bug (issue #1): the discount is truncated, not rounded, so
    # 10% off 2.15 charges 1.94 instead of 1.93.
    off = Decimal(int(off * 100)) / 100
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
