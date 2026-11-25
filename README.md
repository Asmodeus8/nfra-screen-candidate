# A Counter Application

A simple redis-backed web application featuring a hit counter.

## Instructions

The goal of the excercise is to demonstrate your generic troubleshooting, debugging, and refactoring skills across this
repo.  At the end of the exercise, you should be able to run `docker compose up --build`, browse to the app, and see the counter
increment on each page load.

## Steps
run `docker compose up --build` , debug and fix any bugs you find

## Running

```sh
docker compose up --build
```

Open http://localhost:4001. Each page load increments the counter; the button increments it without a reload.

| Endpoint | Method | Result |
| --- | --- | --- |
| `/` | GET | Counter page, increments on load |
| `/api/visits` | GET | `{"visits": n}` without incrementing |
| `/api/visits` | POST | Increments and returns `{"visits": n}` |
| `/health` | GET | `{"status": "ok"}` or 503 if Redis is down |

## What was wrong and how it was fixed

The original stack crashed on startup with `AttributeError: 'NoneType' object has no attribute 'startswith'`.

| # | Problem | Fix |
| --- | --- | --- |
| 1 | Compose set `REDIS-SERVER`, the app reads `REDIS_SERVER`, so the URL was `None` | Renamed to `REDIS_SERVER` |
| 2 | Redis URL pointed to host `redis`, but the service is `redis-server` | `redis://redis-server:6379` |
| 3 | Compose set `SERVERPORT`, the app reads `SERVER_PORT` | Renamed to `SERVER_PORT` |
| 4 | App port was 4001 while compose maps `4001:8081` | App listens on 8081 |
| 5 | Bound to `192.168.1.1`, not an address inside the container | Binds to `0.0.0.0` |
| 6 | `client.set('visits', 0)` reset the count on every app start | Removed; `INCR` starts from 0 on its own |
| 7 | No startup ordering, so the app could start before Redis | Redis healthcheck + `depends_on: service_healthy` |
| 8 | Hard-coded "Listening on port 8081" log line | Removed; gunicorn logs the real bind |

## Improvements

- Gunicorn instead of the Flask development server, running as a non-root user
- Pinned base images (`python:3.13-alpine`, `redis:7-alpine`); unpinned `python:alpine` had already moved to 3.15
- Redis data on a named volume with append-only persistence, so the count survives restarts
- Redis outages return 503 instead of crashing the request
- `restart: unless-stopped` on both services, `.dockerignore`, smaller image layers
- JSON API, health endpoint and a responsive light/dark counter page
