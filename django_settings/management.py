# -*- coding: utf-8 -*-
from django.db.models import signals
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

import django_settings


DEFAULT_SETTINGS = getattr(settings, 'DJANGO_SETTINGS', {})


def initialize_data(sender, **kwargs):
    for name, type_name_and_value in DEFAULT_SETTINGS.items():
        type_name, value = type_name_and_value

        if not django_settings.exists(type_name):
            django_settings.set(type_name, name, value)

signals.post_syncdb.connect(initialize_data, sender=django_settings.models)
