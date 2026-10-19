# Rehearsal Shop

A small shop used to rehearse how [den](https://github.com/wickkit/den) adopts a repo it didn't create.

- `backend/`: FastAPI catalogue, cart and checkout total (`uv sync && uv run pytest -q`).
- `frontend/`: TypeScript cart helpers, tested with Node's built-in runner (`npm ci && npm test`).
- `.github/workflows/ci.yml`: the CI both run in.

One backend test, `test_discount_rounds_half_up`, is red on purpose: it pins a known bug (issue #1) so an adopting tool has a pre-existing failure to record.
