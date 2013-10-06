# -*- coding: utf-8 -*-
# system
import os
import sys
import unittest
from os.path import join, pardir, abspath, dirname


os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.conf'
sys.path.insert(0, abspath(join(dirname(__file__), pardir)))


class AssertQueriesCountMixin(object):
    def assert_queries_count(self, num, func=None, *args, **kwargs):
        from django.test.testcases import _AssertNumQueriesContext
        from django.db import connections, DEFAULT_DB_ALIAS

        using = kwargs.pop("using", DEFAULT_DB_ALIAS)
        conn = connections[using]

        context = _AssertNumQueriesContext(self, num, conn)
        if func is None:
            return None

        with context:
            return func(*args, **kwargs)


class TestCase(unittest.TestCase):
    assert_equal = unittest.TestCase.assertEqual
    assert_not_equal = unittest.TestCase.assertNotEqual
    assert_true = unittest.TestCase.assertTrue
    assert_false = unittest.TestCase.assertFalse
    assert_raises = unittest.TestCase.assertRaises

    def assert_items_equal(self, first, second):
        self.assert_equal(set(first), set(second))


class DBTestCase(TestCase, AssertQueriesCountMixin):
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
