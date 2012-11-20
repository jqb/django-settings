# -*- coding: utf-8 -*-
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType

from . import dataapi, conf, models


DEFAULT_SETTINGS = getattr(conf, 'DJANGO_SETTINGS', {})


def initialize_data(sender, **kwargs):
    for name, type_name_and_value in DEFAULT_SETTINGS.items():
        type_name, value = type_name_and_value

        if not dataapi.data.exists(type_name):
            dataapi.data.set(type_name, name, value)

signals.post_syncdb.connect(initialize_data, sender=models)
