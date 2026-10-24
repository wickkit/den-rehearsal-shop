#!/usr/bin/env bash
# Drill: GET /health answers 200 with {"status":"ok","version":<pyproject version>}.
set -euo pipefail
cd "$(dirname "$0")/../../backend"
uv run --quiet python - <<'EOF'
import tomllib
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

want = tomllib.loads(Path("pyproject.toml").read_text())["project"]["version"]
r = TestClient(app).get("/health")
assert r.status_code == 200, f"status {r.status_code}"
body = r.json()
assert body == {"status": "ok", "version": want}, f"body {body!r}, want version {want!r}"
print(f"PASS health: 200 {body}")
EOF
