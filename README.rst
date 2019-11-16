# Contax
> A simple digital address book.

## Development setup

### Running locally

Dependencies:

- Python 3.6+
- Your virtualenv tool of choice (strongly recommended)
- [Poetry](https://poetry.eustace.io/docs/) dependency manager
- node.js & npm (v6 or later recommended, only required for development)

```bash
# install
$ git clone git@github.com:hmarment/contax.git
$ cd contax
$ mkvirtualenv -p /path/to/python3 contax
$ poetry install

# run db migrations
$ cd contax/backend
$ python manage.py migrate contax

# backend dev server:
python manage.py runserver

# frontend dev server:
$ cd ../frontend
$ npm install
$ npm run start
```