# -*- coding: utf-8 -*-
# test stuff
from . import DBTestCase, n

# tested app
import djsettings

# test app imports
from moduleregistry_testapp import settingsmodels, models


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
        settingsmodels.register()

    def teardown(self):
        models.registry.unregister_all()

    def test_contenttypes_names_should_be_cached(self):
        djsettings.data.clear_cache()
        # NOTE: it clears ALL the cache not only related to djsettings

        assure_db_queries(lambda: djsettings.data.contenttypes_names(), 0)
