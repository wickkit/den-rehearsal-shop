# Rehearsal Shop

A small shop used to rehearse how [den](https://github.com/wickkit/den) adopts a repo it didn't create.

- `backend/`: FastAPI catalogue, cart and checkout total (`uv sync && uv run pytest -q`).
- `frontend/`: TypeScript cart helpers, tested with Node's built-in runner (`npm ci && npm test`).
- `.github/workflows/ci.yml`: the CI both run in.

`test_discount_rounds_half_up` pinned a known bug (issue #1) so an adopting tool had a pre-existing failure to record; den fixed it in v0.2.

## Tests

The same commands CI runs:

```sh
cd backend && uv sync && uv run pytest -q    # needs Postgres; CI starts one as a service
cd frontend && npm ci && npm test            # Node 24 or newer
```
