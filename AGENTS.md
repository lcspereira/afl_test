# Agent instructions

Use [README.md](README.md) for setup, migrations, authentication, and project
development details. See [.github/copilot-instructions.md](.github/copilot-instructions.md)
for the fuller architecture, command, and convention reference.

## Commands

Run backend commands from `backend/`:

```bash
uv run pytest
uv run pytest tests/unit/test_example.py::test_example
uv run ruff check .
uv run ruff format --check .
uv run alembic revision --autogenerate -m "description"
uv run alembic upgrade head
```

Run frontend commands from `frontend/`: `npm run dev`, `npm run build`, and
`npm run lint`.

## Repository-specific rules

- Backend dependencies point inward: `interfaces` → `application` → `domain`;
  `infrastructure` implements persistence and external adapters.
- Import ORM models in `backend/app/infrastructure/database/models/` so
  `Base.metadata` and Alembic autogeneration discover them. Review generated
  migrations before applying them.
- AI agents must not create or modify `test_*.py` files unless explicitly
  asked. Agents may update fixtures such as `conftest.py` and
  `tests/factories/`.
- Authentication uses Argon2 password hashes and bearer JWTs. Do not expose
  password hashes; refresh tokens are rotated once, and production requires a
  unique `JWT_SECRET_KEY`.
