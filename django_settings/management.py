# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from django_settings import models



DEFAULT_SETTINGS = getattr(settings, 'DJANGO_SETTINGS', {})



def initialize_data(sender, **kwargs):
    for name, type_name_and_value in DEFAULT_SETTINGS.items():
        type_name, value = type_name_and_value
        SettingClass = ContentType.objects.get(app_label='django_settings', model=type_name.lower()).model_class()
        
        if not models.Setting.objects.value_object_exists(name):
            models.Setting.objects.set_value(name, SettingClass, value)


def post_migrate_listener(sender, **kwargs):
    if kwargs.get('app') == 'django_settings':
        initialize_data(sender, **kwargs)


try:
    from south.signals import post_migrate
    post_migrate.connect(post_migrate_listener)
except ImportError:
    from django.db.models.signals import post_syncdb
    post_syncdb.connect(initialize_data, sender=models)
