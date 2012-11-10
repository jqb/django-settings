# -*- coding: utf-8 -*-


def import_django_settings():
    from django.conf import settings
    return settings


def autoregister(module_name='settingsmodels', settings=None):
    # framework
    from django.utils.importlib import import_module

    # app public api
    from .api import RegisterError

    settings = settings or import_django_settings()

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)

        try:
            rmod = import_module('%s.%s' % (app, module_name))
        except ImportError:
            pass # Ignore that one
        except RegisterError:
            raise
        else:
            rmod.register()  # registering ONLY on demand

