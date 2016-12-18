# dwitter
Inspired by [arkt.is/t/](http://arkt.is/t/Yy53aWR0aD0yZTM7eC5maWxsUmVjdCgxNTAsMTUwKlModCkrMTUwLDE1MCwxNTAp)

Current build: [dwitter.net](http://dwitter.net)

## Setup
* `make setup` (set up virtual environment)
* `source venv/bin/activate` (activate virtual environment)
* `make` (install dependencies and set up database)
* `make run` run server
* go to localhost:8000/admin and change localhost site to localhost:8000
* in settings/local.py make sure you set SITE_ID correct  (usually 1 or 2) 
* Make sure dweet.localhost:8000/ returns a django error. May not work in Firefox.

## Other commands
* `make migrations`
* `make migrate`
* `make lint`
* `make shell`
* `make thegame`
* `make backup`
