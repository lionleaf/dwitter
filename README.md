# Dwitter Backend

The backend of the Dwitter platform.

[![license](https://img.shields.io/github/license/lionleaf/dwitter.svg)](LICENCE.md)

## What is Dwitter?

Dwitter is a platform to write visual art in JavaScript limited to 140 characters. The name is derived from Twitter, that also allows messages up to 140 characters. This project is inspired by [arkt.is/t/](http://arkt.is/t/Yy53aWR0aD0yZTM7eC5maWxsUmVjdCgxNTAsMTUwKlModCkrMTUwLDE1MCwxNTAp).

## Join us

You can join the Dwitter community on [dwitter.net](http://dwitter.net) or using [Discord](https://discord.gg/r5nXDsQ).

## Get started

### Download

```shellscript
sudo apt install git virtualenv python-pip
git clone https://github.com/lionleaf/dwitter.git
```

### Install

```shellscript
make setup
source venv/bin/activate
make
python manage.py createsuperuser
```

### Run

```shellscript
make run
```

Use this if you're working inside a VM with port forwarding:

```shellscript
make serve
```

### Use

If the server is running, you can access everything. Here are some other commands:

* `make migrations`
* `make migrate`
* `make lint`
* `make shell`
* `make backup`
* `make restore-backup`

## Admin panel

The admin panel is available at http://localhost:8000/admin. You can login with the superuser credentials you made earlier.

## API

The API documentation can be found [here](API_DOCUMENTATION.md).