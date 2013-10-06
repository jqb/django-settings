# -*- coding: utf-8 -*-
"""
djsettings.cache
----------------

a set of tools that makes method caching a little more flexible that simple
`cached` method decorator.

XXX: the whole mechanism should be fixed as now it's too complicated to explain
"""
from .lazyimport import lazyimport

django = lazyimport({
    'settings': 'django.conf',
})
config = lazyimport({
    'DJANGO_SETTINGS_TIMEOUT': 'django_settings.conf',
})


class KeyMaker(object):
    def __init__(self, prefix):
        self.prefix = prefix

    def convert(self, arg):
        if isinstance(arg, unicode):
            return arg.encode(django.settings.DEFAULT_CHARSET)
        else:
            return str(arg)

    def args_to_key(self, args):
        return ":".join(map(self.convert, args))

    def kwargs_to_key(self, kwargs):
        return ":".join([
            "%s:%s" % (self.convert(k), self.convert(v))
            for k, v in kwargs.items()
        ])

    def make(self, method_name, args, kwargs):
        key = ":".join((
            self.prefix,
            method_name,
            self.args_to_key(args),
            self.kwargs_to_key(kwargs),
        ))
        return key


class MethodProxy(object):
    def __init__(self, instance, method):
        self.instance = instance
        self.method = method  # accually it's NOT bounded s it's a function!
        self._keymaker = KeyMaker(prefix='django_settings')

        # NOTE: it's proxy, so let's add at least some basic func properties
        self.func_name = self.method.__name__

    @property
    def cache(self):
        return self.instance.cache  # ATTENTION: this may raise django ImportError

    def origin_method(self, *args, **kwargs):
        return self.method(self.instance, *args, **kwargs)

    def _cache_key(self, args, kwargs):
        return self._keymaker.make(self.method.__name__, args, kwargs)

    def _cache_get(self, key):
        return self.cache.get(key)

    def _cache_set(self, key, origin_value, timeout=None):
        timeout = timeout or config.DJANGO_SETTINGS_TIMEOUT
        self.cache.set(key, origin_value, timeout=timeout)
        return origin_value

    def __call__(self, *args, **kwargs):
        key = self._cache_key(args, kwargs)
        cached_value = self._cache_get(key)
        if cached_value is None:
            origin_value = self.origin_method(*args, **kwargs)
            cached_value = self._cache_set(key, origin_value)
        return cached_value


class cache_method(object):
    def __init__(self, method, method_proxy_class=MethodProxy):
        # NOTE: to be honest... it's not a method but a function
        self.method = method
        self.method_proxy_class = method_proxy_class
        self.method_proxy_name = '_proxy_to_%s' % self.method.__name__

    def __get__(self, instance, instance_type=None):
        proxy = getattr(instance, self.method_proxy_name, None)
        if proxy is None:
            proxy = self.method_proxy_class(instance, self.method)
            setattr(instance, self.method_proxy_name, proxy)
        return proxy
