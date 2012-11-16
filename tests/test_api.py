# -*- coding: utf-8 -*-
# test stuff
from . import DBTestCase, n

# tested app
import django_settings

# test app imports
from moduleregistry_testapp import settingsmodels


class APITest(DBTestCase):
    def before_database_setup(self):
        django_settings.register(settingsmodels.MyString)

    def teardown(self):
        django_settings.unregister_all()

    def test_should_set_properly(self):
        n.assert_true(hasattr(django_settings.models, 'MyString'))

        assert not django_settings.exists('admin_email')
        django_settings.set('MyString', 'admin_email', 'admin@admin.com')
        assert django_settings.get('admin_email') == 'admin@admin.com'
