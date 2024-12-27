CMD_MAKEMIGRATIONS := poetry run python manage.py makemigrations
CMD_MIGRATE := poetry run python manage.py migrate
CMD_START_API := poetry run python manage.py runserver 0.0.0.0:8000

CMD_COVERAGE_RUN := coverage run manage.py test
CMD_COVERAGE_REPORT := coverage report

.PHONY: makemigrations migrate start-api seed-comments unit-test coverage-run coverage-report

makemigrations:
	$(CMD_MAKEMIGRATIONS)

migrate:
	$(CMD_MIGRATE)

start-api:
	$(CMD_MAKEMIGRATIONS)
	$(CMD_MIGRATE)
	$(CMD_START_API)

seed-answers:
	python manage.py seed_answers

unit-test:
	python manage.py test

coverage-run:
	$(CMD_COVERAGE_RUN)

coverage-report:
	$(CMD_COVERAGE_REPORT)

coverage-report-details:
	coverage run manage.py test -v 2
	coverage report

coverage-report-html:
	coverage run manage.py test
	coverage html
	open htmlcov/index.html

build:
	docker compose build

run:
	docker compose up --build

run-db-answer-consumer:
	poetry run python manage.py start_db_answer_consumer

run-redis-answer-consumer:
	poetry run python manage.py start_redis_answer_consumer
