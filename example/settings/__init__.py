# -*- coding: utf-8 -*-
import os

def create_projectpath(thefile):
    from os.path import join, dirname, abspath
    root = abspath(join(dirname(abspath(thefile)), '..'))
    return lambda *a: join(root, *a)

# "Temporary globals" that migth be useful
# It can be used in each settings file as builtin
projectpath = create_projectpath(__file__)


def apps_from(folder, include_name=True, as_list=False):
    """
    Get all names of django-apps in the project in the given directory/module
    Assuming you have only "core" app in "app" directory::

       INSTALLED_APPS = (
           'django.contrib.admin',
       ) + apps_from('app')

       assert INSTALLED_APPS == ('django.contrib.admin', 'app.core')  # => True

    Or if you have "app" folder on the path you can always do this::

       INSTALLED_APPS = (
           'django.contrib.admin',
       ) + apps_from('app', include_name=False)

       assert INSTALLED_APPS == ('django.contrib.admin', 'core')  # => True
    """
    from os.path import join, abspath, exists

    modules = []
    for dname in os.listdir(folder):
        if exists(abspath(join(folder, dname, '__init__.py'))):
            if include_name:
                name = "%s.%s" % (folder, dname)
            else:
                name = "%s" % (dname)
            modules.append(name)

    if as_list:
        return modules

    return tuple(modules)


# sequence of settings module to read
files_base_names = [
    'common',
    os.environ.get('DJANGO_ENV', 'dev'),
    'local_settings'
]

for base_name in files_base_names:
    filepath = '%s/%s.py' % (projectpath('settings'), base_name)
    if os.path.exists(filepath):
        execfile(filepath)

# cleanup
del base_name, files_base_names, filepath, projectpath, create_projectpath
