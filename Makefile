.PHONY: all
all: update migrate

.PHONY: run
run:
	python manage.py runserver

.PHONY: update
update:
	pip install --upgrade -r requirements.txt

.PHONY: migrate
migrate:
	python manage.py migrate

.PHONY: migrations
migrations:
	python manage.py makemigrations

.PHONY: lint
lint:
	flake8 dwitter/ --exclude=migrations,settings

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

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	find . -type d -empty -delete

