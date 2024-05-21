start_db:
	docker-compose up -d image-ticket-db

start_project:
	docker-compose up image-ticket-db backend celery_worker

test:
	docker-compose run test
