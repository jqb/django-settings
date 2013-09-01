django-settings
===============


.. image:: https://badge.fury.io/py/django-settings.png
   :target: https://badge.fury.io/py/django-settings

.. image:: https://api.travis-ci.org/jqb/django-settings.png?branch=master
   :target: https://travis-ci.org/jqb/django-settings


Django reusable application for storing global project settings in database.

By project settings I mean things like admin mail, some default values like
default_post_limit etc. Values are validated depending their type.
Begining with ver 1.3 you can register your own settings values.


Supported versions
------------------

* Python: 2.6, 2.7  (python 2.6 requires importlib)
* Django: 1.3, 1.4, 1.5


API
---

IMPORTANT: changed in version 1.3, old api still works but caching do not work with it.


.. code-block:: python

  import django_settings

  # getting values
  # this will raise django_settings.models.Setting.DoesNotExist
  # exception if value not exists
  # if value is not in cache it will be cached
  django_settings.get('post_limit')

  # if you not sure value exists you can pass "default" parameter,
  # at this point default is NOT cached
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

.. code-block:: bash

   $> pip install django-settings


2) Add "django_settings" to your INSTALLED_APPS

.. code-block:: python

    INSTALLED_APPS = (
        'django.contrib.contenttypes',  # contenttypes framework is required

        # ...

        'django_settings',

        # ...
    )


3) If you want to add your own settings models, please add them in one of your
   applications models file, and register them with django_settings api:

.. code-block:: python

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


There is ability to setup some defaults via project settings.py file.
Those settings will be setup ONLY if they not already exists in db.

.. code-block:: python

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

1.3-4 - setup.py bug fix


1.3-3 beta - python & django various versions compatibility changes


1.3-2 beta - several bug fixes including cache unicode keys handling, tests added


1.3-1 beta - admin render_change_form fix


1.3 beta - several improvements has been made since ver 1.0

    1) setting name need to be unique now (backward incompatiblity)
    2) from now you can extend settings with your own types using
       `django_settings.register` function
    3) new api with caching mechanism introduced
    4) admin interface has been improved, action to clear cache
       keys only used by the package added

    Some tests has been added for core functionality.


Backward incompatible changes

  `django_settings.models.Setting` name need to be unique now, however
  ver 1.3 still allows it to not to be unique. Just set `DJANGO_SETTINGS_UNIQUE_NAMES`
  application setting to False (True is by default).


Author
------

  * Kuba Janoszek (kuba.janoszek@gmail.com)


Contributors
------------

  * `Trey Hunner <https://github.com/treyhunner/>`_
  * `ygneo <https://github.com/ygneo/>`_


