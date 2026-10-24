#!/usr/bin/env bash
# GET /products?sort=price lists products cheapest first; an unknown sort is a 422.
set -euo pipefail
trap 'rc=$?; if [ "$rc" -eq 0 ]; then echo PASS; else echo "FAIL (exit $rc)"; fi' EXIT
cd "$(dirname "$0")/../../backend"
uv run --quiet python - <<'PY'
from fastapi.testclient import TestClient
from app.main import app

c = TestClient(app)
r = c.get("/products?sort=price")
assert r.status_code == 200, r.status_code
got = [(p["id"], p["price"]) for p in r.json()]
want = [("spoon", "2.15"), ("tea", "4.20"), ("mug", "9.99")]
assert got == want, got
prices = [float(p) for _, p in got]
assert prices == sorted(prices), prices
r = c.get("/products?sort=colour")
assert r.status_code == 422, r.status_code
print("cheapest first:", ", ".join(i for i, _ in got))
PY
