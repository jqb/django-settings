# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('django.views.generic',
    (r'^admin/', include(admin.site.urls)),
)
