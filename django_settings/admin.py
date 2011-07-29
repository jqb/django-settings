# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext as _
from django.contrib.contenttypes import generic
from django_settings import models, forms


def get_setting_value(obj):
    return obj.setting_object.value
get_setting_value.short_description = _('Value')


class SettingAdmin(admin.ModelAdmin):
    model = models.Setting
    form = forms.SettingForm
    list_display = ('name', 'setting_type', get_setting_value)
admin.site.register(models.Setting, SettingAdmin)
