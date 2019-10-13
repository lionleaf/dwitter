.PHONY: all
all: install migrate

.PHONY: install
install:
	poetry install
	npm install

.PHONY: run
run:
	poetry run python manage.py runserver

.PHONY: serve
serve:
	poetry run python manage.py runserver 0.0.0.0:8000

.PHONY: update
update:
	poetry update
	npm install

.PHONY: migrate
migrate:
	poetry run python manage.py migrate

.PHONY: migrations
migrations:
	poetry run python manage.py makemigrations

.PHONY: lint
lint: lint-python lint-js-fix lint-css-fix

.PHONY: lint-python
lint-python:
	poetry run flake8 dwitter/ --exclude=migrations,settings

.PHONY: lint-js
lint-js:
	npm run lint -- --max-warnings 0

.PHONY: lint-js-fix
lint-js-fix:
	npm run lint-fix -- --max-warnings 0

.PHONY: lint-css-fix
lint-css-fix:
	npm run css-fix

.PHONY: test
test:
	poetry run python manage.py test

.PHONY: setup
setup:
	cp dwitter/settings/local.py.example dwitter/settings/local.py

.PHONY: shell
shell:
	poetry run python manage.py shell

.PHONY: backup
backup:
	poetry run python manage.py dbbackup

.PHONY: restore-backup
restore-backup:
	poetry run python manage.py dbrestore

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	find . -type d -empty -delete
