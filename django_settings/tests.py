# -*- coding: utf-8 -*-
from django.conf import settings
from django.test import TestCase

from django_settings.models import Setting


DJANGO_SETTINGS = settings.DJANGO_SETTINGS


class SettingDefaults(TestCase):
    def test_default_settings(self):
        """
        Test assuemes that following dict is in your settings.py file:

        DJANGO_SETTINGS = {
           'application_limit': ('Integer', 2),
           'admin_email': ('String', 'kuba.janoszek@gmail.com'),
           }
        """
        value = Setting.objects.get_value('application_limit')
        self.assertEquals(value, DJANGO_SETTINGS['application_limit'][1])
