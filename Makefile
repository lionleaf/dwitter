.PHONY: all
all: update migrate

.PHONY: run
run:
	python manage.py runserver

.PHONY: serve
serve:
	python manage.py runserver 0.0.0.0:8000

.PHONY: update
update:
	pip install --upgrade -r requirements.txt
	npm install

.PHONY: migrate
migrate:
	python manage.py migrate

.PHONY: migrations
migrations:
	python manage.py makemigrations

.PHONY: lint
lint: lint-python lint-js-fix lint-css-fix

.PHONY: lint-python
lint-python:
	flake8 dwitter/ --exclude=migrations,settings

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
	python manage.py test

.PHONY: setup
setup:
	virtualenv venv
	cp dwitter/settings/local.py.example dwitter/settings/local.py

.PHONY: shell
shell:
	python manage.py shell

.PHONY: backup
backup:
	python manage.py dbbackup

.PHONY: restore-backup
restore-backup:
	python manage.py dbrestore

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	find . -type d -empty -delete
