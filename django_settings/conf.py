# -*- coding: utf-8 -*-
from django.conf import settings

DJANGO_SETTINGS_UNIQUE_NAMES = getattr(settings, 'DJANGO_SETTINGS_UNIQUE_NAMES', True)
DJANGO_SETTINGS = getattr(settings, 'DJANGO_SETTINGS', None) or {}

