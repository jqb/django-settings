# -*- coding: utf-8 -*-
# framework
from django.db import models
from django.contrib.contenttypes.models import ContentType
try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except:
    from django.contrib.contenttypes.generic import GenericForeignKey
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
try:
    from django.db.models.signals import post_migrate
except:
    from django.db.models.signals import post_syncdb as post_migrate

from .moduleregistry import new_registry

# app local
from . import conf


class Model(models.Model):  # Base class for db setting
    class Meta:
        abstract = True

    def __unicode__(self):
        return u'%s' % self.value


class SettingManager(models.Manager):
    def get_value(self, name, **kw):
        if 'default' in kw:
            if not self.value_object_exists(name):
                return kw.get('default')
        return self.get(name=name).setting_object.value

    def value_object_exists(self, name):
        queryset = self.filter(name=name)
        return queryset.exists() and queryset[0].setting_object

    def set_value(self, name, SettingClass, value, validate=False):
        setting = Setting(name=name)

        if self.value_object_exists(name):
            setting = self.get(name=name)
            setting_object = setting.setting_object
            setting_object.delete()

        setting_object = SettingClass(value=value)

        if validate:
            setting_object.clean_fields()

        setting_object.save()

        setting.setting_object = setting_object
        setting.save()
        return setting


class Setting(models.Model):
    class Meta:
        verbose_name = _('Setting')
        verbose_name_plural = _('Settings')

    objects = SettingManager()

    setting_type = models.ForeignKey(ContentType)
    setting_id = models.PositiveIntegerField()
    setting_object = GenericForeignKey('setting_type', 'setting_id')

    name = models.CharField(max_length=255, unique=conf.DJANGO_SETTINGS_UNIQUE_NAMES)



# Extentions #######################################################

# we will extend this module dynamicaly via "settingsmodels" modules
registry = new_registry(__name__)

# cleanup
del new_registry
# end ###############################################################


# Builtin settings models
class Email(Model):
    value = models.EmailField()

    class Meta:
        abstract = True
registry.register(Email)


class String(Model):
    value = models.CharField(max_length=254)

    class Meta:
        abstract = True
registry.register(String)


class Integer(Model):
    value = models.IntegerField()

    class Meta:
        abstract = True
registry.register(Integer)


class PositiveInteger(Model):
    value = models.PositiveIntegerField()

    class Meta:
        abstract = True
registry.register(PositiveInteger)
# end ###################


@receiver(post_migrate)
def handle_post_syncdb(sender, **kwargs):
    from django_settings.dataapi import initialize_data
    initialize_data()
