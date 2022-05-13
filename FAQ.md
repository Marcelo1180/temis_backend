# How use git
First init the virtualenv with
```
pipenv shell
```

Second versioning with classic commands of git, in this case will call to pre-commit to run tests
```
(env)$ git add .
(env)$ git commit -m "example commit"
```

Create a new app
```
mkdir ./base/apps/appname
django-admin startapp appname ./base/apps/appname
```
edit apps.py into appname
```
class AppnameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base.apps.appname'
```
