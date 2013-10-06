# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django import template

register = template.Library()


@register.filter
def add_url_for_setting_type(admin_change_list, type_name):
    cl = admin_change_list
    url_name = 'admin:%s_%s_%s' % (cl.opts.app_label, cl.opts.module_name, 'add')
    query = "typename=%(type)s%(popup)s" % dict(
        type=type_name,
        popup='_popup=1' if cl.is_popup else '',
    )
    return '%s?%s' % (reverse(url_name), query)
