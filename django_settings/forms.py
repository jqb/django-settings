# -*- coding: utf-8 -*-
import re
from django import forms
from django.forms.models import modelform_factory
from django.utils.translation import ugettext_lazy as _

from . import api as django_settings


class SettingForm(forms.ModelForm):
    class Meta:
        model = django_settings.db.Setting
        fields = ('name', 'value')

    # this might be predefined with admin interface
    setting_model = None

    value = forms.CharField()

    def clean_name(self):
        """ Check for any other characters apart from alpha numeric chars
        """ 

        name = self.cleaned_data['name']
        res = re.search("[^A-Za-z0-9_]", name)
        if res:
            raise forms.ValidationError("No spaces or special characters allowed in the name")
        
        return name


    def __init__(self, *args, **kwargs):
        super(SettingForm, self).__init__(*args, **kwargs)
        self.fields['value'] = self.setting_model._meta.get_field('value').formfield()

        instance = kwargs.get('instance')
        if instance:
            self.fields['value'].initial = getattr(instance.setting_object, 'value', '')

    def setting_changed(self, instance):
        django_settings.DataAPI.setting_changed(instance)
        return instance

    def save(self, *args, **kwargs):
        cd = self.clean()

        if self.instance and self.instance.setting_id:
            setting_object = self.instance.setting_object
            setting_object.delete()

        setting_object = self.setting_model.objects.create(value=cd['value'])

        kwargs.update(commit=False)
        instance = forms.ModelForm.save(self, *args, **kwargs)
        instance.setting_object = setting_object
        instance.save()
        return self.setting_changed(instance)

