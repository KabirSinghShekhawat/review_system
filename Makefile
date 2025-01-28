initial_migration:
	alembic revision --autogenerate -m "Initial migration"
migrate_db:
	@read -p "Enter revision message: " input; \
	python -m alembic revision --autogenerate -m "$$input"
	python -m alembic upgrade head
apply_migration:
	alembic upgrade head
rollback_migration:
	alembic downgrade -1
install:
	pip install -r requirements.txt
run_server:
	uvicorn app.main:app --reload
run_worker_server:
	celery -A app.tasks worker --loglevel=info
run_redis:
	docker run -d -p 6379:6379 redis
setup_postgres:
	docker run --name reviews_db -e POSTGRES_HOST_AUTH_METHOD='trust' -e POSTGRES_PASSWORD='' -e POSTGRES_USER='admin' -e POSTGRES_DB='reviews_db' -p 127.0.0.1:5432:5432  -d postgres:14
