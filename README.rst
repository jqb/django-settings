django-settings
===============

Current version: 1.3 beta


Django reusable application for storing global project settings in database.

By project settings I mean things like admin mail, some default values like
default_post_limit etc. Values are validated depending their type.
Begining with ver 1.3 you can register your own settings values.


API
---

IMPORTANT: changed in version 1.3, old api still works but caching do not work
with it.

::

  import django_settings

  # getting values
  django_settings.get('post_limit')
  django_settings.get('post_limit', default=10)

  # set values - cache is updated for "get" and "exists" method
  # values are validated using setting_value model clean_fields method
  django_settings.set('Email', 'admin_email', 'admin@admin.com')

  # If you want to avoid validation, do this:
  django_settings.set('Email', 'admin_email', 'admin@admin.com', validate=False)

  # checking if value exists
  django_settings.exists('admin_email')



Installation & setup
--------------------

1) Install it using pip:

::

   $> pip install django-settings


2) Add "django_settings" to your INSTALLED_APPS

::

    INSTALLED_APPS = (
        'django.contrib.contenttypes',  # contenttypes framework is required

        # ...

        'django_settings',

        # ...
    )


3) If you want to add your own settings models, please add them in one of your
   applications models file, and register them with django_settings api:

::

   # <project>/<app>/models.py
   from django.db import models


   # ... your application models


   import django_settings

   class Text(django_settings.db.Model):
       value = models.TextField()
       class Meta:
           abstract = True   # it's IMPORTANT - it need to be abstract
   django_settings.register(Text)


Remember to define model as abstract, this is important because of how django
treats model classes.


When ``register`` function will be invoked all your models will be available in
``django_settings.models`` module, so django can treat them as regular models.


There is ability to setup some defaults via project settings.py file.
Those settings will be setup ONLY if they not exists in db yet.

::

   DJANGO_SETTINGS = {
      'application_limit': ('Integer', 2),
      'admin_email': ('String', 'admin@mail.com'),
   }


Settings types
--------------

Builidin settings types: Email, Integer, String, PositiveInteger


Admin
-----

You can manipulate setting via your admin interface.


Changelog
---------

1.2 beta - two big things has been changed.

    1) from now you can extend settings with your own types
    2) new api with caching mechanism introduced

    Some tests has been added for core functionality.
    It's possible to use old API but there's no cache.

