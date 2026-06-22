# Structured Investment Platform

A production-ready full-stack platform for managing structured investment products, portfolio holdings, and transactions.

## Tech Stack

- Backend: FastAPI, PostgreSQL, SQLAlchemy ORM, Alembic-ready metadata, JWT auth
- Frontend: React, Vite, Tailwind CSS
- Testing: Pytest, React Testing Library-ready setup
- Deployment: Docker, Render, Vercel, Neon PostgreSQL

## Project Structure

```text
backend/
  app/
    core/          # settings, security, database
    models/        # SQLAlchemy ORM models
    routers/       # FastAPI route modules
    schemas/       # Pydantic request/response schemas
    services/      # business logic and persistence operations
    utils/         # reusable helpers and dependencies
    main.py        # FastAPI application factory
  tests/           # backend unit/API tests
frontend/
  src/
    api/           # API client
    components/    # reusable UI components
    pages/         # routed pages
    context/       # auth state
```

## Local Development

1. Copy environment files:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

2. Run with Docker:

```bash
docker compose up --build
```

3. Open:

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Frontend: http://localhost:5173

The API creates tables on startup for this starter. For larger production systems, add Alembic migrations before changing schemas.

## Backend Without Docker

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend Without Docker

```bash
cd frontend
npm install
npm run dev
```

## Tests

```bash
cd backend
pytest
```

```bash
cd frontend
npm run lint
```

## Deployment

### Neon PostgreSQL

Create a Neon project and copy the pooled PostgreSQL connection string. Use it as `DATABASE_URL` in Render.

### Render

Use `render.yaml`. Set these secrets in Render:

- `DATABASE_URL`
- `SECRET_KEY`
- `BACKEND_CORS_ORIGINS`

### Vercel

Deploy `frontend/` as the project root and set:

- `VITE_API_URL=https://your-render-api.onrender.com`

