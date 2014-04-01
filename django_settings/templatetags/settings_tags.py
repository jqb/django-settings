# -*- coding: utf-8 -*-
from django import template
import django_settings

register = template.Library()

@register.tag
def settings(parser, token):
    tag_name, format_string = token.split_contents()
    if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    return template.TextNode(django_settings.get(format_string[1:-1]))
