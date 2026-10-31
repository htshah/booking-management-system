.PHONY: up down build logs seed ps restart clean

up:
	docker compose up --build -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

seed:
	docker compose exec backend uv run python -m app.seed

ps:
	docker compose ps

restart: down up

clean:
	docker compose down -v
