# -*- coding: utf-8 -*-
# test stuff
from . import TestCase, n


class ModelRegisterTest(TestCase):
    def test_importing_special_module_should_add_all_registered_classes(self):
        # before special module import
        from .moduleregistry_testapp import models
        n.assert_false(hasattr(models, 'MyString'))
        n.assert_not_in('MyString', models.registry)

        # import special module that triggers registering
        from .moduleregistry_testapp import settingsmodels
        settingsmodels.register()

        n.assert_true(hasattr(models, 'MyString'))
        n.assert_in('MyString', models.registry)

        n.assert_not_equal(
            models.MyString.__module__,
            settingsmodels.MyString.__module__,
        )

        # technicaly those models are not the same
        n.assert_not_equal(models.MyString, settingsmodels.MyString)
        n.assert_true(issubclass(models.MyString, settingsmodels.MyString))

        # registered class became a part of the module
        n.assert_equal(models.MyString.__module__, models.__name__)

        models.registry.unregister_all()
        n.assert_false(hasattr(models, 'MyString'))

