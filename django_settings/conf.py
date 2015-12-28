# -*- coding: utf-8 -*-
from django.conf import settings
from .keymaker import KeyMaker

DJANGO_SETTINGS_UNIQUE_NAMES = getattr(settings, 'DJANGO_SETTINGS_UNIQUE_NAMES', True)
DJANGO_SETTINGS_TIMEOUT = getattr(settings, 'DJANGO_SETTINGS_TIMEOUT', 60 * 60 * 24 * 1)  # one day
DJANGO_SETTINGS_CACHE_KEYMAKER = getattr(settings, 'DJANGO_SETTINGS_CACHE_KEYMAKER', KeyMaker)
DJANGO_SETTINGS = getattr(settings, 'DJANGO_SETTINGS', None) or {}
