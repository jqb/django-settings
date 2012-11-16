# -*- coding: utf-8 -*-
# test stuff
from . import DBTestCase, n

# tested app
import django_settings


def assure_db_queries(function, num):
    from django import db

    before = len(db.connection.queries)
    result = function()
    after  = len(db.connection.queries)

    queries_count = after - before
    if queries_count != num:
        raise Exception("Number of queries: %d, but expected: %s" % (queries_count, num))

    return result


class DataCachingTest(DBTestCase):
    def before_database_setup(self):
        from moduleregistry_testapp import settingsmodels

    def teardown(self):
        from moduleregistry_testapp import models
        models.registry.unregister_all()

    def test_contenttypes_names_should_be_cached(self):
        django_settings.data.clear_cache()
        # NOTE: it clears ALL the cache not only related to django_settings

        assure_db_queries(lambda: django_settings.data.contenttypes_names(), 0)
