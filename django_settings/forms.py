# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Q
from django.forms.models import modelform_factory
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from django_settings import models


class SettingForm(forms.ModelForm):
    class Meta:
        model = models.Setting
        fields = ('setting_type', 'name')

    value = forms.CharField()

    def __init__(self, *a, **kw):
        forms.ModelForm.__init__(self, *a, **kw)
        self.fields['setting_type'].queryset = ContentType.objects.filter(
            Q(name='string') | Q(name='integer') | Q(name='positive integer'))

        instance = kw.get('instance')
        if instance:
            self.fields['value'].initial = getattr(instance.setting_object, 'value', '')

    def clean(self):
        cd = self.cleaned_data
        SettingClass = cd['setting_type'].model_class()
        SettingClassForm = modelform_factory(SettingClass)

        value = cd.get('value')
        if not value:
            self._errors['value'] = self.error_class(['Value field cannot be empty.'])
        else:
            setting_form = SettingClassForm({'value': cd['value']})
            if not setting_form.is_valid():
                del cd['value']
                self._errors['value'] = self.error_class(['Value is not valid.'])
        return cd

    def save(self, *args, **kwargs):
        cd = self.clean()

        if self.instance and self.instance.setting_id:
            setting_object = self.instance.setting_object
            setting_object.delete()

        SettingClass = cd['setting_type'].model_class()
        setting_object = SettingClass.objects.create(value=cd['value'])

        kwargs['commit'] = False
        instance = forms.ModelForm.save(self, *args, **kwargs)
        instance.setting_id = setting_object.id
        instance.save()
        return instance
