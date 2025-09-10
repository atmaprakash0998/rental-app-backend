# Backend - FastAPI with PostgreSQL (Feature-based)

## Environment variables

Create a `.env` file in `backend/` with:

```
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=rentalapp

# Optional for alembic (override runtime URL)
ALEMBIC_DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rentalapp
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Migrations

Initialize DB and run migrations:

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

`alembic/env.py` targets `app.core.db.Base` and reads DB URLs from env.

## Run server

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

## Structure

```
backend/
  main.py                 # Entrypoint: imports app.main:app
  app/
    main.py               # FastAPI app, CORS, includes routers
    core/
      config.py           # Env-based settings
      db.py               # SQLAlchemy async engine/session, Base
    features/
      items/
        controller.py     # Routes
        service.py        # Business logic
        models.py         # SQLAlchemy models
        schemas.py        # Pydantic schemas
  alembic/
    env.py                # Migration environment
    versions/             # Generated revisions
  alembic.ini             # Alembic config
  requirements.txt
```

## Notes


