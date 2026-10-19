import { test } from "node:test";
import assert from "node:assert/strict";
import { badge, cents, formatCents, subtotal, type Item } from "./cart.ts";

const items: Item[] = [
  { id: "tea", name: "Green tea", price: "4.20" },
  { id: "mug", name: "Blue mug", price: "9.99" },
];

test("cents parses decimal strings", () => {
  assert.equal(cents("4.20"), 420);
  assert.equal(cents("9.9"), 990);
  assert.equal(cents("3"), 300);
});

test("formatCents pads", () => {
  assert.equal(formatCents(1839), "$18.39");
  assert.equal(formatCents(5), "$0.05");
});

test("subtotal sums lines", () => {
  assert.equal(subtotal(items, { tea: 2, mug: 1 }), 1839);
});

test("subtotal rejects unknown items", () => {
  assert.throws(() => subtotal(items, { kettle: 1 }));
});

test("badge caps at 99+", () => {
  assert.equal(badge({}), "");
  assert.equal(badge({ tea: 3 }), "3");
  assert.equal(badge({ tea: 120 }), "99+");
});
