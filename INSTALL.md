# INSTALL Temis backend

Setup config settings

```sh
cp .env.example .env
```

**DEBUG=true** is used for debugging mode, in this mode you can use:

- admin/ (Classic admin of django)
- apidoc/ (Swagger api documentation)
- logging with level DEBUG

## Installing in DEVELOPMENT MODE

Installing general and dev dependencies

```sh
pipenv install --ignore-pipfile --dev
```

Access to the virtualenv

```sh
pipenv shell
```

Run migrations

```sh
(env)$ python manage.py migrate
(env)$ python manage.py migrate account
```

Create a super user

```sh
(env)$ python manage.py createsuperuser
```

## Installing in PRODUCTION MODE

In production mode settings.json its important to set **DEBUG=false**

Installing dependencies

```sh
pipenv install --ignore-pipfile
```

Run migrations

```sh
(env)$ python manage.py migrate
(env)$ python manage.py migrate account
```

Create a super user

```sh
(env)$ python manage.py createsuperuser
```

Demon service install

```sh
cd /etc/systemd/system
sudo ln -s <path root project>/main.service .
```

Start service

```sh
sudo service main start
```

Watch logs

```sh
sudo journalctl -e -u main.service
```
