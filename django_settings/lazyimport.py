# -*- coding: utf-8 -*-
import importlib  # requires python 2.7


class lazyimport(object):
    """
    Usage::

        from lazyimport import lazyimport

        django = lazyimport({
            'ContentType' : 'django.contrib.contenttypes.models',
            'cache'       : 'django.core.cache',
        })

        django.ContentType  # importing takes place here
        django.cache        # importing takes place here
    """

    def __init__(self, mapping):
        self.__mapping = mapping

    def __getattr__(self, name):
        mapping = self.__mapping
        if name in mapping:
            imported = getattr(importlib.import_module(mapping[name]), name)
            setattr(self, name, imported)
            return imported
        return object.__getattribute__(self, name)
