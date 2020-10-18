# dwitter

A platform to write visual art in javascript limited to 140 characters.

The frontend is currently being rewritten, so please direct frontend development to [dwitter-frontend](https://www.github.com/dwitter-net/dwitter-frontend).
The new frontend is currently hosted at [beta.dwitter.net](https://beta.dwitter.net).

Available on [dwitter.net](https://www.dwitter.net)

Join the chat on [Discord](https://discord.gg/r5nXDsQ)

[![license](https://img.shields.io/github/license/lionleaf/dwitter.svg)]()

Inspired by [arkt.is/t/](http://arkt.is/t/Yy53aWR0aD0yZTM7eC5maWxsUmVjdCgxNTAsMTUwKlModCkrMTUwLDE1MCwxNTAp)


## Pre-requisites and first-time installation
* Install `npm`
* `sudo apt install npm`
*  Get packages needed for server and clone the repository
* `sudo apt install git virtualenv python-pip`
* `git clone https://github.com/lionleaf/dwitter.git`

## Setup
#### **Linux**
1. `make setup` (set up virtual environment)
2. `source venv/bin/activate` (activate virtual environment)
3. `make` (install dependencies and set up database)
4. `python manage.py createsuperuser` (create admin account used below)
5. `make run` runs the server. Use `make serve` instead if you're working inside a VM with port forwarding. (0.0.0.0:8000)
6. Go to [http://localhost:8000/admin/sites/](http://localhost:8000/admin/sites/) and log in with admin account created above.
7. Click on the one entry, and change both `domain name` and `display name` to localhost:8000.
8. Make sure http://dweet.localhost:8000/ returns a django error. May not work in Firefox.

#### **Windows**
1. Download the latest [python3.7 release]("https://www.python.org/downloads/windows/").
2. Without installing the setup, extract all the files in the a new directory such as `./python37`
3. Set up virtual environment using the extracted interpreter: `virtualenv --python ./python37/python.exe venv`
4. Activate the venv: `cd venv/Scripts && activate.bat`
5. Get back in the main directory (`cd ../.. && make`) and use `make` command (install dependencies and set up database)
6. Continue with the fourth step from **Linux setup**.

## Other commands
* `make migrations`
* `make migrate`
* `make lint`
  * lints Python and JS files
  * automatically fixes some JS issues (mostly whitespace-related)
* `make shell`
* `make backup`
* `make restore-backup`


# Dwitter API

### Dweets
```
GET www.dwitter.net/api/dweets/  - list of the last 10 dweets

       ?limit=100            - number of results to return, default 10, max 100 (subject to change)
       &offset=200           - offset page by 200 dweets
       &remix_of=123         - all remixes of 123
       &author=lionleaf      - dweets by author


GET www.dwitter.net/api/dweets/123  - get details about d/123
```

Latest dweet: `https://www.dwitter.net/api/dweets/?limit=1`  (sorted by posted date by default)


### Users
```
GET dwitter.net/api/users/lionleaf  - Show details about user 'lionleaf'.
```
