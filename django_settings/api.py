# -*- coding: utf-8 -*-
# Public module API
from .moduleregistry import RegisterError  # noqa
from .dataapi import DataAPI, data  # noqa
from .lazyimport import lazyimport

# shortcuts
get = data.get
set = data.set
exists = data.exists
all = data.all
type_names = data.type_names


# django settings-dependent parts should be loadded lazily
db = lazyimport({  # this is also part of public api
    'Model': 'django_settings.models',
    'Setting': 'django_settings.models',
    'registry': 'django_settings.models',
})

# expose methods


def register(*a, **kw):
    db.registry.register(*a, **kw)


def unregister(*a, **kw):
    db.registry.unregister(*a, **kw)


def unregister_all(*a, **kw):
    db.registry.unregister_all(*a, **kw)
