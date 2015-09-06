# -*- coding: utf-8 -*-
# module
from .cache import cache_method, MethodProxy
from .lazyimport import lazyimport
from . import conf


# lazy imports
django = lazyimport({
    'ContentType': 'django.contrib.contenttypes.models',
    'cache': 'django.core.cache',
    'Q': 'django.db.models',
})
db = lazyimport({
    'registry': 'django_settings.models',
    'Setting': 'django_settings.models',
})


class dataapi_set_method_proxy(MethodProxy):
    def __call__(self, type_name, name, value, validate=True, timeout=None):
        get_key = self._keymaker.make('get', [name], {})
        exists_key = self._keymaker.make('exists', [name], {})
        value_to_cache = self.origin_method(type_name, name, value, validate=validate)
        cached_value = self._cache_set(get_key, value_to_cache, timeout=timeout)
        self._cache_set(exists_key, True, timeout=timeout)
        return cached_value


NIL = type('NIL', (object,), {})()


class dataapi_get_method_proxy(MethodProxy):
    def __call__(self, name, **kwargs):
        default = kwargs.pop('default', NIL)
        try:
            return super(dataapi_get_method_proxy, self).__call__(name)
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

    def __init__(self, cache_client=None):
        self._client = cache_client

    @property
    def cache(self):  # as lazy as possible
        return self._client or django.cache

    def contenttypes_names(self):
        ctypes = django.ContentType.objects.filter(
            django.Q(app_label="django_settings") & ~django.Q(name="Setting")
        )
        return [ct.name for ct in ctypes]
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
        setting = db.Setting.objects.set_value(name, setting_type, value, validate=validate)
        return setting.setting_object.value
    set = cache_method(set, dataapi_set_method_proxy)

    def exists(self, name):
        return bool(db.Setting.objects.value_object_exists(name))
    exists = cache_method(exists)

    def all(self):
        names = db.Setting.objects.values_list('name', flat=True)
        items = [(name, self.get(name)) for name in names]
        return dict(items)

    def clear_cache(self):
        self.cache.clear()

    # XXX: fix this mechanism
    def _set_cache_for(self, name, value):
        get_key = self.get._cache_key([name], {})
        exists_key = self.exists._cache_key([name], {})
        self.get._cache_set(get_key, value)
        self.exists._cache_set(exists_key, True)


data = DataAPI()


# initialize data
DEFAULT_SETTINGS = getattr(conf, 'DJANGO_SETTINGS', {})


def initialize_data():
    for name, type_name_and_value in DEFAULT_SETTINGS.items():
        type_name, value = type_name_and_value

        if not data.exists(name):
            data.set(type_name, name, value)
