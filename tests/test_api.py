# -*- coding: utf-8 -*-
# test stuff
from . import DBTestCase

# tested app
import django_settings

# test app imports
from .moduleregistry_testapp import settingsmodels


class APITest(DBTestCase):
    def before_database_setup(self):
        django_settings.register(settingsmodels.MyString)

    def teardown(self):
        django_settings.unregister('MyString')

    def test_should_set_properly(self):
        self.assert_true(hasattr(django_settings.models, 'MyString'))

        assert not django_settings.exists('admin_email')
        django_settings.set('MyString', 'admin_email', 'admin@admin.com')
        assert django_settings.get('admin_email') == 'admin@admin.com'

    def test_get_should_accept_default_param(self):
        result = django_settings.get('unexisting_value', default="DefaultValue")
        self.assert_equal(result, "DefaultValue")

    def test_get_should_raise_DoesNotExist_if_theres_no_such_setting(self):
        self.assert_raises(
            django_settings.db.Setting.DoesNotExist,
            lambda: django_settings.get('unexisting_value'),
        )

    def test_setting_value_few_times(self):
        typename = "MyString"
        django_settings.set(typename, 'test_string', 'data1')
        self.assert_equal(django_settings.exists('test_string'), True)
        self.assert_equal(django_settings.get("test_string"), "data1")

        django_settings.set(typename, 'test_string', 'data2')
        self.assert_equal(django_settings.data.get("test_string"), "data2")

        django_settings.set(typename, 'test_string', 'data3')
        self.assert_equal(django_settings.data.get("test_string"), "data3")

        django_settings.set(typename, 'test_string', 'data4')
        self.assert_equal(django_settings.data.get("test_string"), "data4")
