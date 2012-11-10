# -*- coding: utf-8 -*-
from django.db import models


class Integer(object):
    value = models.IntegerField()


def register():
    from .models import registry
    registry.register(Integer)

