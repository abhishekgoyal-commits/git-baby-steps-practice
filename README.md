# Jira Sprint Dashboard

Runnable scaffolding for the Jira sprint dashboard specification.

## Prerequisites

- Node.js 22 or newer
- npm 11 or newer
- Docker Desktop with Docker Compose enabled for PostgreSQL

## Run Locally

Install dependencies once:

```powershell
Push-Location backend; npm install; Pop-Location
Push-Location frontend; npm install; Pop-Location
```

Start the backend:

```powershell
Push-Location backend; npm start; Pop-Location
```

The backend health endpoint is available at `http://localhost:3001/api/health`.

Start the frontend in another terminal:

```powershell
Push-Location frontend; npm run dev -- --host 127.0.0.1; Pop-Location
```

Open `http://127.0.0.1:5173/` to view the dashboard shell.

## Run With Docker Compose

Install and start Docker Desktop, then run:

```powershell
docker compose up --build
```

This starts PostgreSQL 15 on port `5432`, the backend on port `3001`, and the frontend on port `5173`. Verify PostgreSQL after startup with:

```powershell
docker compose exec db pg_isready -U jira_dashboard -d jira_dashboard
```

The current backend and frontend are health-check scaffolds. Jira integration, migrations, and dashboard data retrieval are planned follow-up tasks.
