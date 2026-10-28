# Rally Courts (Learning Project)

> **Educational use only.** This is a deliberately simple, from-scratch sample app built to practice FastAPI, PostgreSQL, SQLAlchemy and React basics. It is intentionally written the way a new grad developer might write it: no authentication, no caching, no database optimization (indexes, pooling, migrations), and no production hardening. Do not use this as a reference for building a real, production-grade system.

## What this is

A tiny court-booking app with two features:

1. **List available courts** — browse courts by name, sport type, address, and hours.
2. **My bookings** — see your past bookings and create a new one.

There is no login or signup. Instead, a random ID is generated in the browser (stored in `localStorage`) and sent to the backend as a `user_id` to identify "who" is booking. This is not secure and is only meant to keep the exercise simple.

## Repo structure

```
backend/     FastAPI + PostgreSQL API (Python)
frontend/    React + Vite single-page app (JavaScript)
```

### Backend (`backend/`)

- `app/main.py` — FastAPI app setup, CORS, routes
- `app/database.py` — SQLAlchemy engine/session setup
- `app/models.py` — `Court` and `Booking` ORM models
- `app/schemas.py` — Pydantic request/response models
- `app/routers/` — `courts.py` and `bookings.py` route handlers
- `app/seed.py` — inserts a handful of sample courts

Tables are created automatically on startup via `Base.metadata.create_all()` — there are no migrations (e.g. Alembic) in this project, again to keep things simple.

### Frontend (`frontend/`)

- `src/pages/CourtsPage.jsx` — lists available courts
- `src/pages/BookingsPage.jsx` — shows past bookings and a form to create a new one
- `src/api.js` — plain `fetch` calls to the backend
- `src/userId.js` — generates/reads the random `user_id` from `localStorage`

## Running locally

### 1. Database

You need a local PostgreSQL instance. The quickest way is Docker:

```bash
docker run --name rally-courts-db -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=rally_courts -p 5432:5432 -d postgres
```

### 2. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # adjust DATABASE_URL if needed

python -m app.seed             # seed sample courts
uvicorn app.main:app --reload  # runs on http://localhost:8000
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev   # runs on http://localhost:5173
```

Open `http://localhost:5173` in your browser.

## API endpoints

| Method | Path                     | Description                        |
| ------ | ------------------------ | ----------------------------------- |
| GET    | `/courts`                | List all courts                     |
| GET    | `/courts/{court_id}`     | Get a single court                  |
| GET    | `/bookings?user_id=...`  | List bookings for a given user      |
| POST   | `/bookings`              | Create a new booking                |

## What this is good for

- Learning how a FastAPI app is wired together (routers, Pydantic schemas, SQLAlchemy sessions, dependency injection).
- Practicing a simple relational model (`Court` and `Booking`, one-to-many) with SQLAlchemy.
- Learning basic React data fetching with `useState`/`useEffect`, forms, and client-side routing.
- Seeing a minimal full-stack app end to end: database → API → UI.

## What this is **not**

- Not an example of authentication, authorization, or secure identity (the `user_id` is just a client-generated UUID — anyone can impersonate anyone).
- Not an example of database optimization, indexing strategy, or migrations.
- Not an example of caching, background jobs, payments, notifications, or any of the production concerns a real booking platform would need.
