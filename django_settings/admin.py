# -*- coding: utf-8 -*-
# framework
from django.contrib import admin
from django.utils.translation import ugettext as _
from django.contrib.contenttypes import generic

# module local
from . import models, forms, dataapi


def get_setting_value(obj):
    # return obj.setting_object.value
    return dataapi.data.get(obj.name)
get_setting_value.short_description = _('Value')


class SettingAdmin(admin.ModelAdmin):
    model = models.Setting
    form = forms.SettingForm
    list_display = ('name', 'setting_type', get_setting_value)


admin.site.register(models.Setting, SettingAdmin)

