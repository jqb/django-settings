# -*- coding: utf-8 -*-
from django.db import models
import djsettings


class String(djsettings.Model):
    value = models.CharField(max_length=512)

    class Meta:
        abstract = True


def register():
    from .models import registry
    registry.register(String)

