# Copilot instructions

## Build, test, and lint

Run backend commands from `backend/`:

```bash
uv sync
uv run uvicorn app.main:app --reload
uv run pytest
uv run pytest tests/unit/test_example.py::test_example
uv run ruff check .
uv run ruff format --check .
uv run alembic revision --autogenerate -m "description"
uv run alembic upgrade head
```

The pytest selector can also target a class or a specific test in any test
file. Backend packages require Python 3.12 or newer.

Run frontend commands from `frontend/`:

```bash
npm install
npm run dev
npm run build
npm run lint
```

`build` runs the TypeScript project build before Vite. For the complete
containerized application, run `docker compose up --build` from the repository
root.

## Architecture

- The backend follows inward dependency direction: `interfaces` adapts HTTP
  requests and responses, `application` contains use-case services and ports,
  `domain` owns framework-independent contracts and exceptions, and
  `infrastructure` implements persistence and other external adapters.
- `backend/app/main.py:create_app` is the composition root. It accepts settings,
  creates the SQLAlchemy engine and session factory, stores the factory on app
  state, initializes the database in the lifespan, and registers middleware,
  exception handlers, and routers.
- Alembic configuration lives in `backend/alembic.ini` and migration scripts in
  `backend/migrations/`. Its environment reads the database URL from backend
  settings and uses `Base.metadata`; import new ORM models in the database
  models package so autogeneration can discover them.
- Authentication is implemented by the application `AuthService`, with Argon2
  password hashing and JWT signing/verification in infrastructure. Refresh
  tokens are persisted and rotated once at `/auth/refresh`. Keep password
  hashes out of API responses; protected routes use bearer tokens, and
  production must use a unique `JWT_SECRET_KEY`.
- API dependencies construct application services from request-scoped database
  sessions. Routers validate and serialize through Pydantic schemas; keep
  persistence details out of the service and domain layers.
- The frontend flows from `App.tsx` and page/components to services. Services
  use the shared `getJson` client, and API contracts live in `src/types/`.
  Endpoint paths passed to the client are relative to the configured API URL;
  `VITE_API_URL` includes the `/api/v1` prefix.
- Docker Compose runs the backend and frontend separately, waits for backend
  health before starting the frontend, and persists SQLite data in the
  `backend-data` volume.

## Repository conventions

- Keep Python dependencies pointing inward. Define external requirements as
  application ports or domain repository contracts, and implement them under
  `infrastructure`; wire implementations through FastAPI dependencies.
- Use `create_app(settings)` and the test fixtures for isolated app/database
  setup. Tests use pytest, `TestClient`, and SQLAlchemy sessions; SQLite
  foreign-key enforcement is enabled by the engine setup.
- Follow the backend's Ruff configuration: Python 3.12 target, 79-character
  line length, and the configured `E`, `W`, `F`, `I`, `N`, `B`, and `UP` rules.
- Keep frontend API access in `src/services/`, share the configured client,
  and represent API payloads with TypeScript types in `src/types/`. Shared MUI
  styling is configured in `src/theme.ts`.
- Source comments and user-facing API text follow the existing Portuguese
  convention.
- The README sets a TDD policy and specifies that AI agents must not create or
  modify `test_*.py` files unless explicitly asked. Agents may create or modify
  test fixtures such as `conftest.py` and `tests/factories/`.
