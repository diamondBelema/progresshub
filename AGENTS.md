# Progress Hub v2

FastAPI + HTMY + Tailwind CSS v4 goal-tracking web app with Appwrite backend and OpenRouter AI coaching.

## Quick start

```bash
uv sync                # install Python deps
npm install            # install Tailwind CLI
npx @tailwindcss/cli -i static/assets/tailwind.css -o static/assets/styles.css
uv run uvicorn app.main:app --reload
```

Copy `.env.example` to `.env` and fill in Appwrite credentials (endpoint, project ID, API key, database ID, collection IDs).

## Commands

| Action | Command |
|---|---|
| Run dev server | `uv run uvicorn app.main:app --reload` |
| Lint | `uv run ruff check` |
| Typecheck | `uv run mypy .` |
| Test (all) | `uv run pytest` |
| Test (single file) | `uv run pytest tests/test_routes.py -v` |
| Rebuild CSS | `npx @tailwindcss/cli -i static/assets/tailwind.css -o static/assets/styles.css` |
| Add CSS classes | Edit `static/assets/tailwind.css`, then rebuild. Also add to `app/components/_safelist.py` if dynamically constructed at runtime. |

Run `ruff check -> mypy . -> pytest` in this order before committing.

## Architecture

- `app/main.py` — FastAPI app entrypoint, mounts routes and static files
- `app/core/config.py` — Settings from `.env` via `pydantic-settings`
- `app/routes/` — Route handlers (auth, goals, checkin, dashboard, onboarding, settings, public, leaderboard)
- `app/services/` — `appwrite.py` (DB client), `openrouter.py` (AI plan/insight generation)
- `app/repositories/` — Data access (goal_repo, checkin_repo, user_repo)
- `app/schemas/` — Dataclasses (Goal, CheckIn, User) with `from_doc` / `to_dict`
- `app/components/` — HTMY UI components, `ui.py` has inlined replacements for FastTailwind
- `app/utils/cn.py` — Class name utility (`cn("a", False, "b")` → `"a b"`)
- `app/htmy.py` — Global `HTMY()` instance, used via `@htmy.page()` decorator on handlers

Auth is cookie-based (`user_id` cookie set on login), checked manually in each route handler.

## Testing quirks

- `tests/conftest.py` adds project root to `sys.path`
- `tests/test_routes.py` requires server running on `http://127.0.0.1:9999`; skips module-level if unavailable. Tests public route status codes and protected routes that should redirect to login.
- `tests/test_components.py` tests import/instantiation only (no rendering). Schemas are dataclasses constructed directly.
- Integration tests need real Appwrite credentials in `.env` and access to the Appwrite instance.

## Conventions

- All Python files start with `from __future__ import annotations`
- Schemas are `@dataclass` with `from_doc(cls, doc_id, data)` classmethod and `to_dict()` method
- JSON fields in Appwrite docs are stored as strings, deserialized with `json.loads()` in `from_doc`
- Components use `htmy` library with `@htmy.page()` decorator returning a `PageShell` wrapper
- Tailwind v4 is used — no `tailwind.config.js`, theme defined via `@theme` directive in `tailwind.css`
- UI components define their own variant-to-Tailwind-class maps (no external dependency)
- All UI component classes go through `cn()` utility from `app.utils.cn`

## .env

```env
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=
APPWRITE_API_KEY=
OPENROUTER_API_KEY=
SECRET_KEY=
APPWRITE_DATABASE_ID=
APPWRITE_PROFILES_COLLECTION_ID=users_profile
APPWRITE_SESSIONS_COLLECTION_ID=sessions
APPWRITE_GOALS_COLLECTION_ID=goals
APPWRITE_CHECKINS_COLLECTION_ID=checkins
```
