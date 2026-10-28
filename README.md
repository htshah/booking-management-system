# Rally Courts (Learning Project)

> **Educational use only.** This is a deliberately simple, from-scratch sample app built to practice FastAPI, PostgreSQL, SQLAlchemy and React basics. It is intentionally written the way a new grad developer might write it: no authentication, no caching, no database optimization (indexes, pooling, migrations), and no production hardening. Do not use this as a reference for building a real, production-grade system.

## What this is

A tiny court-booking app with two features:

1. **List available courts** — browse courts by name, sport type, address, and hours. Click into a court to view its details, pick a date, and select one or more open time slots to book.
2. **My bookings** — see your upcoming and past bookings.

There is no login or signup. Instead, a random ID is generated in the browser (stored in `localStorage`) and sent to the backend as a `user_id` to identify "who" is booking. This is not secure and is only meant to keep the exercise simple.

## Repo structure

```
backend/            FastAPI + PostgreSQL API (Python)
frontend/           React + Vite single-page app (JavaScript)
docker-compose.yml  db + backend + frontend containers
Makefile            `make up` / `make down` wrapper around docker compose
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
- `src/pages/CourtDetailPage.jsx` — court details, date picker, and time-slot booking
- `src/pages/BookingsPage.jsx` — shows upcoming and past bookings
- `src/api.js` — plain `fetch` calls to the backend
- `src/userId.js` — generates/reads the random `user_id` from `localStorage`

## Running locally

### Option A: Docker Compose (recommended)

This spins up Postgres, the backend, and the frontend together.

```bash
make up     # builds images and starts db, backend, frontend in the background
make seed   # one-time: insert sample courts
make logs   # tail logs from all services
make down   # stop and remove the containers
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Postgres: localhost:5432 (user `postgres`, password `postgres`, db `rally_courts`)

Both `backend/` and `frontend/` are bind-mounted into their containers, so code changes on your machine are picked up automatically (uvicorn `--reload` and Vite's dev server).

See the [`Makefile`](Makefile) for other targets (`build`, `ps`, `restart`, `clean`).

### Option B: Run everything manually

#### 1. Database

You need a local PostgreSQL instance. The quickest way is Docker:

```bash
docker run --name rally-courts-db -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=rally_courts -p 5432:5432 -d postgres
```

#### 2. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # adjust DATABASE_URL if needed

python -m app.seed             # seed sample courts
uvicorn app.main:app --reload  # runs on http://localhost:8000
```

#### 3. Frontend

```bash
cd frontend
npm install
npm run dev   # runs on http://localhost:5173
```

Open `http://localhost:5173` in your browser.

## API endpoints

| Method | Path                                      | Description                                      |
| ------ | ------------------------------------------ | ------------------------------------------------- |
| GET    | `/courts`                                  | List all courts                                   |
| GET    | `/courts/{court_id}`                       | Get a single court                                 |
| GET    | `/courts/{court_id}/availability?date=...` | List time slots for a court on a date (fixed 6am-10pm, 1-hour slots) and whether each is available |
| GET    | `/bookings?user_id=...`                    | List bookings for a given user                    |
| POST   | `/bookings`                                | Create a new booking for one slot                  |

## What this is good for

- Learning how a FastAPI app is wired together (routers, Pydantic schemas, SQLAlchemy sessions, dependency injection).
- Practicing a simple relational model (`Court` and `Booking`, one-to-many) with SQLAlchemy.
- Learning basic React data fetching with `useState`/`useEffect`, forms, and client-side routing.
- Seeing a minimal full-stack app end to end: database → API → UI.

## What this is **not**

- Not an example of authentication, authorization, or secure identity (the `user_id` is just a client-generated UUID — anyone can impersonate anyone).
- Not an example of database optimization, indexing strategy, or migrations.
- Not an example of caching, background jobs, payments, notifications, or any of the production concerns a real booking platform would need.
