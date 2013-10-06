# -*- coding: utf-8 -*-
# test stuff
from . import TestCase

# tested app
import django_settings


# We want to cache, so cannot use django.core.cache.backands.DummyCache
# since it just implement interface and it's not doing anything.
class DictCache(object):
    def __init__(self):
        self.storage = {}

    def get(self, key):
        return self.storage.get(key)

    def set(self, key, value, timeout):
        self.storage[key] = value


class FakeObject(object):
    def __init__(self):
        self.counter = 0
        self.cache = DictCache()

    def fakemethod(self, arg1, arg2, kw1=None, kw2=None):
        self.counter += 1
        return u"Very expensive computation result"
    fakemethod = django_settings.cache.cache_method(fakemethod)
    # default method proxy is django_settings.cache.MethodProxy


class MethodProxyTest(TestCase):
    def setUp(self):
        self.object = FakeObject()
        self.mproxy = self.object.fakemethod

    def test__args_to_key__with_unicode_chars(self):
        arg1 = u'ąśżźć'  # some polish characters
        arg2 = u'ół'
        arg3 = True
        arg1_encoded = '\xc4\x85\xc5\x9b\xc5\xbc\xc5\xba\xc4\x87'
        arg2_encoded = '\xc3\xb3\xc5\x82'
        arg3_encoded = 'True'

        key = self.mproxy._keymaker.args_to_key([arg1, arg2, arg3])
        expected = '%s:%s:%s' % (arg1_encoded, arg2_encoded, arg3_encoded)

        self.assert_equal(key, expected)
        self.assert_equal(key.__class__, str)

    def test__kwargs_to_key__with_unicode_chars(self):
        kw_key = u'key'  # nobodys using unicode var names as funtion params, right?
        kw_val = u'ół'
        kw_key_encoded = 'key'
        kw_val_encoded = '\xc3\xb3\xc5\x82'

        key = self.mproxy._keymaker.kwargs_to_key({
            kw_key: kw_val,
        })
        expected = '%s:%s' % (kw_key_encoded, kw_val_encoded)

        self.assert_equal(key, expected)
        self.assert_equal(key.__class__, str)

    def test_should_cache_method_result(self):
        self.assert_equal(self.object.counter, 0)

        args = [u'ąśżźć', u'ół']
        kwargs = {'kw1': u'ąśżźć', 'kw2': u'ół'}

        self.mproxy(*args, **kwargs)  # invocation & cache
        self.assert_equal(self.object.counter, 1)

        self.mproxy(*args, **kwargs)  # should be taken from cache
        self.assert_equal(self.object.counter, 1)
