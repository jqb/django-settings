# -*- coding: utf-8 -*-
# test stuff
from . import DBTestCase, n

# tested app
import djsettings

# test app imports
from moduleregistry_testapp import settingsmodels


class APITest(DBTestCase):
    def before_database_setup(self):
        djsettings.register(settingsmodels.String)

    def teardown(self):
        djsettings.unregister_all()

    def test_should_set_properly(self):
        n.assert_true(hasattr(djsettings.models, 'String'))

        assert not djsettings.exists('admin_email')
        djsettings.set('String', 'admin_email', 'admin@admin.com')
        assert djsettings.get('admin_email') == 'admin@admin.com'
