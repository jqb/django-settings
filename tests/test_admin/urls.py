# -*- coding: utf-8 -*-
import django
if django.VERSION < (1, 6):
    from django.conf.urls.defaults import patterns, include
else:
    from django.conf.urls import patterns, include
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('django.views.generic',
    (r'^admin/', include(admin.site.urls)),
)
