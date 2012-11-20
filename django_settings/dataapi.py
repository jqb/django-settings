# -*- coding: utf-8 -*-
# system
from operator import attrgetter

# module
from .cache import cache_method, MethodProxy
from .lazyimport import lazyimport


# lazy imports
django = lazyimport({
    'ContentType' : 'django.contrib.contenttypes.models',
    'cache'       : 'django.core.cache',
    'Q'           : 'django.db.models',
})
db = lazyimport({
    'registry' : 'django_settings.models',
    'Setting'  : 'django_settings.models',
})


class dataapi_set_method_proxy(MethodProxy):
    def __call__(self, type_name, name, value, validate=True):
        get_key      = self._cache_key_for_method('get', name)
        exists_key   = self._cache_key_for_method('exists', name)
        setting      = self.origin_method(type_name, name, value, validate=validate)
        cached_value = self._cache_set(get_key, setting.setting_object.value)
        self._cache_set(exists_key, True)
        return cached_value


NIL = type('NIL', (object,), {})()


class dataapi_get_method_proxy(MethodProxy):
    def _cache_key(self, name): # should accept only "name"
        return self._cache_key_for_method('get', name)

    def __call__(self, name, **kwargs):
        default = kwargs.pop('default', NIL)
        try:
            return super(dataapi_get_method_proxy, self).__call__(name, **kwargs)
        except db.Setting.DoesNotExist:
            if default != NIL:
                return default
            raise


class DataAPIMetaclass(type):
    registry = []

    def setting_changed(cls, new_setting):
        for inst in cls.registry:  # XXX: the whole mechanism should be changed
            inst._set_cache_for(new_setting.name, new_setting.setting_object.value)

    def __call__(cls, *args, **kwargs):
        new = type.__call__(cls, *args, **kwargs)
        cls.registry.append(new)
        return new


class DataAPI(object):
    __metaclass__ = DataAPIMetaclass

    # class level
    name_getter = attrgetter('name')

    def __init__(self, cache_client=None):
        self._client = cache_client

    @property
    def cache(self):  # as lazy as possible
        return self._client or django.cache

    def contenttypes_names(self):
        ctypes = django.ContentType.objects.get_for_models(*db.registry.values()).values()
        return map(self.name_getter, ctypes)
    contenttypes_names = cache_method(contenttypes_names)

    def contenttypes_queryset(self):
        query = django.Q()
        for name in self.contenttypes_names():
            query = query | django.Q(name=name)
        return django.ContentType.objects.filter(query)

    def model_for_name(self, name):
        return db.registry[name]

    def type_names(self):
        return db.registry.names()

    def get(self, name, **kw):
        return db.Setting.objects.get_value(name, **kw)
    get = cache_method(get, dataapi_get_method_proxy)

    def set(self, type_name, name, value, validate=True):
        setting_type = db.registry.elements[type_name]
        return db.Setting.objects.set_value(name, setting_type, value, validate=validate)
    set = cache_method(set, dataapi_set_method_proxy)

    def exists(self, name):
        return bool(db.Setting.objects.value_object_exists(name))
    exists = cache_method(exists)

    def clear_cache(self):
        self.cache.clear()

    # XXX: fix this mechanism
    def _set_cache_for(self, name, value):
        self.get._cache_set(value, name)


data = DataAPI()

