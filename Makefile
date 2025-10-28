.PHONY: start-celery
start-celery:
	@echo "Starting Celery server"
	celery -A backend.api.service.celery_config worker -P solo --loglevel=info

.PHONY: start-redis
start-redis:
	@echo "Starting Redis server"
	redis-server

.PHONY: start-docker-fresh
start-docker-fresh:
	@echo "Starting and building Docker Containers"
	docker compose up --build -d

.PHONY: start-docker
start-docker:
	@echo "Starting and building Docker Containers"
	docker compose up -d

.PHONY: stop-docker-full
stop-docker-full:
	@echo "Stoping Docker Containers and removing volumes"
	docker compose down -v

.PHONY: stop-docker
stop-docker:
	@echo "Stoping Docker Containers"
	docker compose down