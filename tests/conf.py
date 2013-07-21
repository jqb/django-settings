# -*- coding: utf-8 -*-
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}


INSTALLED_APPS = (
    'django.contrib.contenttypes',

    'django_settings',

    'tests.moduleregistry_testapp',
)


SECRET_KEY = 'secret'
