# Contax
> A simple digital address book.

## Development setup

### Running locally

Dependencies:

- Python 3.6+
- Your virtualenv tool of choice (strongly recommended)
- [Poetry](https://poetry.eustace.io/docs/) dependency manager
- node.js & npm (v6 or later recommended, only required for development)
- Vue.js

```bash
# install
$ git clone git@github.com:hmarment/contax.git
$ cd contax
$ mkvirtualenv -p /path/to/python3 contax
$ poetry install
```

Set up a Postgres database:
```bash
$ psql
$ CREATE DATABASE contax;
$ CREATE USER contax WITH PASSWORD 'password';
$ ALTER ROLE contax SET client_encoding TO 'utf8';
$ ALTER ROLE contax SET default_transaction_isolation TO 'read committed';
$ ALTER ROLE contax SET timezone TO 'UTC';
$ GRANT ALL PRIVILEGES ON DATABASE contax TO contax;
```

Add a .env file containing your Postgres password:
```bash
echo "DB_PASSWORD=password" > .env
```

Run migrations and launch server:
```bash
# run db migrations
$ cd contax/backend
$ python manage.py migrate contacts

# backend dev server:
python manage.py runserver

# frontend dev server:
$ cd ../frontend
$ npm install
$ npm run start
```
