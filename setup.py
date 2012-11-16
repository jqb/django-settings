# -*- coding: utf-8 -*-
import os

from setuptools import setup
import djsettings


setup(
    name='django-settings',
    version=djsettings.__version__,
    description='Simple django reusable application for storing project settings in database.',
    author='Kuba Janoszek',
    author_email='kuba.janoszek@gmail.com',
    url='http://github.com/jqb/django-settings',
    packages=['django_settings'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
)

