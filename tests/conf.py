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


# For test_admin only:
import os


def here(*path):
    absolute_here = os.path.abspath(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(absolute_here, *path))


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.admin',
) + INSTALLED_APPS

TEMPLATE_DIRS = (
    here('test_admin', 'templates'),
)

ROOT_URLCONF = 'tests.test_admin.urls'

DJANGO_SETTINGS_TIMEOUT = 2  # one second
