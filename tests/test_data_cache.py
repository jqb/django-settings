# -*- coding: utf-8 -*-
# test stuff
from . import DBTestCase, n

# tested app
import django_settings


class DataCachingTest(DBTestCase):
    def setup(self):
        django_settings.data.clear_cache()

    def teardown(self):
        django_settings.data.clear_cache()

    def test_contenttypes_names_should_be_cached(self):
        def get_contenttypes_names():
            django_settings.data.contenttypes_names()
        self.assert_queries_count(1, get_contenttypes_names)

    def test_should_run_queries_only_for_save(self):
        def setting_up_setting():
            cached_value = django_settings.data.set('Integer', 'test-1', 1)
            n.assert_equal(cached_value, 1)

        def getting_setting():
            cached_value = django_settings.data.get('test-1')
            n.assert_equal(cached_value, 1)

        def checking_existence_of_setting():
            exists = django_settings.data.exists('test-1')
            n.assert_true(exists)

        # django should run 4 queries for us here:
        # 1) check if *setting* object exists (if yes -
        #    delete it, but it's not the case here)
        # 2) check if *setting.setting_object* exists
        # 3) create new *setting.setting_object* object
        # 4) create new *setting* object
        self.assert_queries_count(4, setting_up_setting)

        # and then getting and checking existence of setting takes no queries
        self.assert_queries_count(0, getting_setting)
        self.assert_queries_count(0, checking_existence_of_setting)

        # ...even if you ask many times...
        for _ in xrange(10):
            self.assert_queries_count(0, getting_setting)
            self.assert_queries_count(0, checking_existence_of_setting)
