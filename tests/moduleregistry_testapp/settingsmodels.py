# -*- coding: utf-8 -*-
from django.db import models
import django_settings


class MyString(django_settings.db.Model):
    value = models.CharField(max_length=512)

    class Meta:
        abstract = True


def register():
    from .models import registry
    registry.register(MyString)
