# -*- coding: utf-8 -*-
"""
djsettings.cache
----------------

a set of tools that makes method caching a little more flexible that simple
`cached` method decorator.

XXX: the whole mechanism should be fixed as now it's too complicated to explain
"""


class MethodProxy(object):
    def __init__(self, instance, method):
        self.key_prefix = 'django_settings'
        self.instance = instance
        self.method = method  # accually it's NOT bounded s it's a function!

        # NOTE: it's proxy, so let's add at least some basic func properties
        self.func_name = self.method.func_name

    @property
    def cache(self):
        return self.instance.cache  # ATTENTION: this may raise django ImportError

    def origin_method(self, *args, **kwargs):
        return self.method(self.instance, *args, **kwargs)

    def _args_to_key(self, args):
        return ":".join([str(val) for val in args])

    def _kwargs_to_key(self, kwargs):
        return ":".join(["%s:%s" % (k,v) for k, v in kwargs.items()])

    def _cache_key_for_method(self, method_name, *args, **kwargs):
        key = ":".join((
            self.key_prefix,
            method_name,
            self._args_to_key(args),
            self._kwargs_to_key(kwargs),
        ))
        return key

    def _cache_key(self, *args, **kwargs):
        return self._cache_key_for_method(self.method.__name__, *args, **kwargs)

    def _cache_get(self, *args, **kwargs):
        key = self._cache_key(*args, **kwargs)
        return self.cache.get(key)

    def _cache_set(self, origin_value, *args, **kwargs):
        key = self._cache_key(*args, **kwargs)
        self.cache.set(key, origin_value)
        return origin_value

    def __call__(self, *args, **kwargs):
        cached_value = self._cache_get(*args, **kwargs)
        if cached_value is None:
            origin_value = self.origin_method(*args, **kwargs)
            cached_value = self._cache_set(origin_value, *args, **kwargs)
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

