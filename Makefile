.PHONY: up down logs migrate

up:
	docker-compose up --build

down:
	docker-compose down

logs:
	docker-compose logs -f

migrate:
	docker-compose exec main-api alembic upgrade head

init-migrations:
	docker-compose exec main-api alembic init migrations
	docker-compose exec main-api alembic revision --autogenerate -m "initial"