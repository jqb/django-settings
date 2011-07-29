# -*- coding: utf-8 -*-
from django.conf import settings
from django.test import TestCase

from django_settings.models import Setting

DJANGO_SETTINGS = settings.DJANGO_SETTINGS


class SettingDefaults(TestCase):
    def test_settings(self):
        """Test assumes that a properly formatted DJANGO_SETTINGS dict is in your settings.py"""
        for key in DJANGO_SETTINGS:
            value = Setting.objects.get_value(key)
            self.assertEquals(value, DJANGO_SETTINGS[key][1])
