# dwitter

[![Join the chat at https://gitter.im/lionleaf/dwitter](https://badges.gitter.im/lionleaf/dwitter.svg)](https://gitter.im/lionleaf/dwitter?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![license](https://img.shields.io/github/license/lionleaf/dwitter.svg)]()

Inspired by [arkt.is/t/](http://arkt.is/t/Yy53aWR0aD0yZTM7eC5maWxsUmVjdCgxNTAsMTUwKlModCkrMTUwLDE1MCwxNTAp)

Current build: [dwitter.net](http://dwitter.net)

## Pre-requisites and first-time installation
* Install `npm`
* `sudo apt install git virtualenv python-pip`
* `git clone https://github.com/lionleaf/dwitter.git`

## Setup
* `make setup` (set up virtual environment)
* `source venv/bin/activate` (activate virtual environment)
* `make` (install dependencies and set up database)
* `python manage.py createsuperuser` (create admin account used below)
* `make run` runs the server. Writing `python manage.py 0.0.0.0:8000` will expose the app if you're working inside a VM with port forwarding.
* go to [http://localhost:8000/admin/sites/](http://localhost:8000/admin/sites/), login with admin account created above, click on the one entry, and change both `domain name` and `display name` to localhost:8000.
* Make sure http://dweet.localhost:8000/ returns a django error. May not work in Firefox.

## Other commands
* `make migrations`
* `make migrate`
* `make lint`
* `make shell`
* `make backup`
* `make restore-backup`
