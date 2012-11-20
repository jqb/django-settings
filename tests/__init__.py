# -*- coding: utf-8 -*-
# system
import os
import re
import sys
import unittest
from os.path import join, pardir, abspath, dirname

# tools
import nose


os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.conf'
sys.path.insert(0, abspath(join(dirname(__file__), pardir)))


TestCase = unittest.TestCase
n        = nose.tools


class DBTestCase(TestCase):
    test_runner, old_config = None, None

    def setUp(self):
        from django.test.simple import DjangoTestSuiteRunner
        self.test_runner = DjangoTestSuiteRunner()
        self.before_environment_setup()                       # HOOK
        self.test_runner.setup_test_environment()
        self.before_database_setup()                          # HOOK
        self.old_config = self.test_runner.setup_databases()
        self.setup()

    def tearDown(self):
        self.test_runner.teardown_databases(self.old_config)
        self.test_runner.teardown_test_environment()
        self.teardown()  # just to make it look like pep8

    def before_environment_setup(self):
        pass

    def before_database_setup(self):
        pass

    def setup(self):
        pass

    def teardown(self):
        pass
# ##############################################################

