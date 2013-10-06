# -*- coding: utf-8 -*-
# test stuff
from . import TestCase


class ModelRegisterTest(TestCase):
    def test_importing_special_module_should_add_all_registered_classes(self):
        # before special module import
        from .moduleregistry_testapp import models
        self.assert_false(hasattr(models, 'MyString'))
        self.assert_false('MyString' in models.registry)

        # import special module that triggers registering
        from .moduleregistry_testapp import settingsmodels
        settingsmodels.register()

        self.assert_true(hasattr(models, 'MyString'))
        self.assert_true('MyString' in models.registry)

        self.assert_not_equal(
            models.MyString.__module__,
            settingsmodels.MyString.__module__,
        )

        # technicaly those models are not the same
        self.assert_not_equal(models.MyString, settingsmodels.MyString)
        self.assert_true(issubclass(models.MyString, settingsmodels.MyString))

        # registered class became a part of the module
        self.assert_equal(models.MyString.__module__, models.__name__)

        models.registry.unregister('MyString')
        self.assert_false(hasattr(models, 'MyString'))
