# -*- coding: utf-8 -*-
from django.db import models
import django_settings


class Text(django_settings.db.Model):
    value = models.TextField()
    class Meta:
        abstract = True
django_settings.register(Text)

