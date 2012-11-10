django-settings
===============

Current version: 1.3 beta


Simple django reusable application for storing global project settings in database.

By project settings I mean things like admin mail, some default values like
default_post_limit etc. Values are validated depending their type.
Begining with ver 1.3 you can register your own settings values.


API
---

IMPORTANT: changed in version 1.3, old api still works but caching do not work
with it.

::

  import djsettings  # or: import django_settings

  # getting values
  djsettings.get('post_limit')
  djsettings.get('post_limit', default=10)

  # set values - cache is updated for "get" and "exists" method
  # values are validated using setting_value model clean_fields method
  djsettings.set('Email', 'admin_email', 'admin@admin.com')

  # If you want to avoid validating do this:
  djsettings.set('Email', 'admin_email', 'admin@admin.com', validate=False)

  # checking if value exists
  djsettings.exists('admin_email')



Installation & setup
--------------------

1) Install it using pip:

::

   $> pip install django-settings


2) Add "djsettings" to your INSTALLED_APPS

::

    INSTALLED_APPS = (
        # ...

        'djsettings',

        # ...
    )


3) Register all settings models on your urls module:

::

   # <project>/urls.py
   from django.conf.urls.defaults import patterns, include
   from django.contrib import admin

   import djsettings

   admin.autodiscover()
   djsettings.autoregister()  # NOTE: do it AFTER admin.autodiscover

   # ...


4) If you want to add your own setting model, create "settingsmodels.py" file in one
of your applications and define your own solutions:

::

    # <project>/<your-app>/settingsmodule.py
    from django.db import models
    import djsettings


    class MyText(djsettings.Model):
        value = models.TextField()
        class Meta:
            abstract = True


    def register():  # create "register" function and add your own models there
        djsettings.register(MyText)


Remember to define this model as abstract, this is important because of how django
treats model classes.


When ``register`` function will be invoked all your models will be available in
``djsettings.models`` module, so django can treat them as regular models.


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

Now you can manipulate setting via your admin interface.
Just remember to put "admin.autodiscover" BEFORE "djsettings.autoregister"
in your "urls.py" file.


Changelog
---------

1.3 beta - three big things has been changed.

    1) package import name changed, old one still exists for backward compatibility
    2) from now you can extend settings with your own types
    3) new api with caching mechanism introduced

    Some tests has been added for core functionality.

    Really important thing is that old api through "django_settings" root
    still works, but it do not support caching.

