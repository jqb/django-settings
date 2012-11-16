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

# ATTENTION: This may vary on your system!
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

