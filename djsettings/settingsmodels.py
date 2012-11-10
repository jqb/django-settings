# -*- coding: utf-8 -*-
# Builtin settings models

# framework
from django.db import models

# public api localy, normally should be: import djsettings
from . import api as djsettings


class Email(djsettings.Model):
    value = models.EmailField()
    class Meta:
        abstract = True


class String(djsettings.Model):
    value = models.CharField(max_length=254)
    class Meta:
        abstract = True


class Integer(djsettings.Model):
    value = models.IntegerField()
    class Meta:
        abstract = True


class PositiveInteger(djsettings.Model):
    value = models.PositiveIntegerField()
    class Meta:
        abstract = True


def register():
    djsettings.register(String)
    djsettings.register(Email)
    djsettings.register(Integer)
    djsettings.register(PositiveInteger)

