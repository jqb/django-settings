# -*- coding: utf-8 -*-
# framework
from django.contrib import admin
from django.contrib.admin.views import main as admin_views
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from django.http import Http404


# module local
from . import models, forms, dataapi


class ChangeList(admin_views.ChangeList):
    @property
    def available_settings_models(self):
        return dataapi.data.type_names()


# Additional columns
def get_setting_value(obj):
    return dataapi.data.get(obj.name)
get_setting_value.short_description = _('Value')
# end


# Actions
def clear_cache(modeladmin, request, queryset):
    data = dataapi.data
    cache_keys = []
    add_key = cache_keys.append
    for name in queryset.values_list('name', flat=True):
        add_key(data.get._cache_key(name))
        add_key(data.exists._cache_key(name))
    data.cache.delete_many(cache_keys)
clear_cache.short_description = _("Clear cache for settings")
# end


class SettingAdmin(admin.ModelAdmin):
    model = models.Setting
    form = forms.SettingForm
    list_display = ('name', 'setting_type', get_setting_value)
    search_fields = ('name', 'setting_type__name')
    actions = [
        clear_cache
    ]

    def get_setting_model(self, obj, request):
        if obj:
            return obj.setting_object.__class__
        try:
            typename = request.REQUEST['typename']        # NOTE: both lines might
            return dataapi.data.model_for_name(typename)  # raise KeyError
        except KeyError:
            raise Http404

    def get_form(self, request, obj=None, **kwargs):
        Form = super(SettingAdmin, self).get_form(request, obj=obj, **kwargs)
        Form.setting_model = self.get_setting_model(obj, request)
        return Form

    def get_changelist(self, request, **kwargs):
        return ChangeList

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        setting_model = self.get_setting_model(obj, request)
        context['setting_model_name'] = setting_model.__name__
        response = super(SettingAdmin, self).render_change_form(
            request, context, add=add, change=change, form_url=form_url, obj=obj)
        return response


admin.site.register(models.Setting, SettingAdmin)

