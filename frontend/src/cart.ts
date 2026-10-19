export interface Item {
  id: string;
  name: string;
  price: string;
}

export type Lines = Record<string, number>;

// Prices come from the API as decimal strings; keep money in cents here.
export function cents(price: string): number {
  const [whole, frac = ""] = price.split(".");
  return Number(whole) * 100 + Number((frac + "00").slice(0, 2));
}

export function formatCents(c: number): string {
  return `$${Math.floor(c / 100)}.${String(c % 100).padStart(2, "0")}`;
}

export function subtotal(items: Item[], lines: Lines): number {
  const byId = new Map(items.map((i) => [i.id, i]));
  let sum = 0;
  for (const [id, qty] of Object.entries(lines)) {
    const item = byId.get(id);
    if (!item) throw new Error(`unknown item ${id}`);
    sum += cents(item.price) * qty;
  }
  return sum;
}

export function badge(lines: Lines): string {
  const n = Object.values(lines).reduce((a, b) => a + b, 0);
  return n === 0 ? "" : n > 99 ? "99+" : String(n);
}
