# -*- coding: utf-8 -*-
# test stuff
from . import DBTestCase

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
            self.assert_equal(cached_value, 1)

        def getting_setting():
            cached_value = django_settings.data.get('test-1')
            self.assert_equal(cached_value, 1)

        def checking_existence_of_setting():
            exists = django_settings.data.exists('test-1')
            self.assert_true(exists)

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

    def test_getting_all_should_not_run_any_queries(self):
        data = [
            ("Integer", "test-int", 1),
            ("String", "test-str", "Value"),
            ("Email", "test-email", "admin@admin.com"),
        ]
        data_dict = dict([
            (name, value) for _, name, value in data
        ])

        def set_all_data():
            for type_name, name, value in data:
                django_settings.set(type_name, name, value)

        def get_all_data():
            self.assert_items_equal(django_settings.all(), data_dict)

        self.assert_queries_count(len(data) * 4, set_all_data)
        self.assert_queries_count(1, get_all_data)  # one query for all names

    def test_should_cache_only_for_configurable_amount_of_time(self):
        self.assert_equal(django_settings.conf.DJANGO_SETTINGS_TIMEOUT, 2)

        original_method = django_settings.data.cache.set

        def set_method_assure_timeout_passing(key, origin_value, timeout=None):
            self.assert_equal(timeout, django_settings.conf.DJANGO_SETTINGS_TIMEOUT)
            return original_method(key, origin_value, timeout=timeout)

        django_settings.data.cache.set = set_method_assure_timeout_passing

        django_settings.set('Email', 'test_email', 'test@email.com')
        django_settings.data.cache.set = original_method
