# -*- coding: utf-8 -*-
# test stuff
from . import TestCase, n

# tested app
import djsettings


class ModelRegisterTest(TestCase):
    def test_importing_special_module_should_add_all_registered_classes(self):
        # before special module import
        from moduleregistry_testapp import models
        n.assert_false(hasattr(models, 'String'))
        n.assert_not_in('String', models.registry)

        # import special module that triggers registering
        from moduleregistry_testapp import settingsmodels
        settingsmodels.register()

        n.assert_true(hasattr(models, 'String'))
        n.assert_in('String', models.registry)

        n.assert_not_equal(
            models.String.__module__,
            settingsmodels.String.__module__,
        )

        # technicaly those models are not the same
        n.assert_not_equal(models.String, settingsmodels.String)
        n.assert_true(issubclass(models.String, settingsmodels.String))

        # registered class became a part of the module
        n.assert_equal(models.String.__module__, models.__name__)

        models.registry.unregister_all()
        n.assert_false(hasattr(models, 'String'))


    def test_autoregister_helper_should_invoke_register_for_all_installed_apps(self):
        djsettings.autoregister('for_autoregistry_test')

        # after autoregistration "models" should contains Integer class
        # take a look at tests.moduleregistry_testapp.for_autoregistry_test
        from moduleregistry_testapp import models

        n.assert_true(hasattr(models, 'Integer'))

        # check if removing works
        models.registry.unregister_all()
        n.assert_false(hasattr(models, 'Integer'))

