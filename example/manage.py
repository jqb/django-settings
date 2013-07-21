#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import site


def setup(root=None, settings_module_name=None):
    """
    Simple setup snippet that makes easy to create
    fast sandbox to try new things.

    :param root: the root of your project
    :param settings_module_name: name of settings module eg:
         "project.setting"

    Usage:
    >>> import manage
    >>> manage.setup()
    >>> # from now on paths are setup, and django is configured
    >>> # you can use it in separate "sandbox" script just to check
    >>> # things really quick
    """
    from django.utils.importlib import import_module
    from django.core.management import setup_environ

    root = os.path.dirname(os.path.abspath(root or __file__))
    path = lambda *a: os.path.join(root, *a)
    settings_module_name = settings_module_name or 'settings'

    # 1) try to import module
    settings = import_module(settings_module_name)

    # 2) setup pythonpath
    if os.path.exists(path('lib')):
        site.addsitedir(path('lib'))

    # 2) cofigure django
    setup_environ(settings)


if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

    from django.core.management import execute_manager
    setup()

    try:
        import settings # Assumed to be in the same directory.
    except ImportError, e:
        import sys
        sys.stderr.write(
            "Error: Can't find the file 'settings.py' in the directory"
            " containing %r. It appears you've customized things.\nYou'll have to"
            " run django-admin.py, passing it your settings module.\n(If the file"
            " settings.py does indeed exist, it's causing an ImportError somehow.)"
            "\nError was %s" % (__file__, e))
        sys.exit(1)
    execute_manager(settings)
