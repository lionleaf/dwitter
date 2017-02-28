# dwitter

[![Join the chat at https://gitter.im/lionleaf/dwitter](https://badges.gitter.im/lionleaf/dwitter.svg)](https://gitter.im/lionleaf/dwitter?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![license](https://img.shields.io/github/license/lionleaf/dwitter.svg)]()

Inspired by [arkt.is/t/](http://arkt.is/t/Yy53aWR0aD0yZTM7eC5maWxsUmVjdCgxNTAsMTUwKlModCkrMTUwLDE1MCwxNTAp)

Current build: [dwitter.net](http://dwitter.net)

## Setup
* `make setup` (set up virtual environment)
* `source venv/bin/activate` (activate virtual environment)
* `make` (install dependencies and set up database)
* `make run` run server
* go to localhost:8000/admin and change localhost site to localhost:8000
* Make sure dweet.localhost:8000/ returns a django error. May not work in Firefox.

## Other commands
* `make migrations`
* `make migrate`
* `make lint`
* `make shell`
* `make backup`
