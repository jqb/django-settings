# -*- coding: utf-8 -*-
from django import template
import re
import django_settings

register = template.Library()


class ContextNode(template.base.TextNode):
    def __init__(self, s, var_name):
        super(ContextNode, self).__init__(s)
        self.var_name = var_name

    def render(self, context):
        if self.var_name:
            context[self.var_name] = self.s
            return ''
        return super(ContextNode, self).render(context)


@register.tag
def settings(parser, token):
    var_name = None
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires arguments" % token.contents.split()[0])
    m = re.search(r'(.*?) as (\w+)', arg)
    if m:
        arg, var_name = m.groups()
    if not (arg[0] == arg[-1] and arg[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name)
    return ContextNode(django_settings.get(arg[1:-1]), var_name)
