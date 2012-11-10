# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include
from django.contrib import admin

import djsettings

admin.autodiscover()
djsettings.autoregister()


urlpatterns = patterns('django.views.generic',
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'simple.direct_to_template', {'template': 'base.html'}),
)
