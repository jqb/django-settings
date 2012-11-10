# -*- coding: utf-8 -*-
# framework
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _


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
    setting_object = generic.GenericForeignKey('setting_type', 'setting_id')

    name = models.CharField(max_length=255)


# Extentions #######################################################
from .moduleregistry import new_registry

# we will extend this module dynamicaly via "settingsmodels" modules
registry = new_registry(__name__)

# cleanup
del new_registry

