PROJECT_ROOT = projectpath()
SECRET_KEY = 'v0_a+905e5a=p^8-tk7qjw9hoqc!hlv72edl0yqlp9^fq@!3tl'

ROOT_URLCONF = 'settings.urls'
TIME_ZONE = 'Europe/Warsaw'
LANGUAGE_CODE = 'en'

DEBUG = True
TEMPLATE_DEBUG = True
ADMINS = ()
MANAGERS = ()

USE_I18N = True
USE_L10N = True

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'debug_toolbar',
    'django_settings',

) + apps_from('app')


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # debuging middleware
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'staticserve.middleware.StaticServe',
    'staticserve.middleware.MediaServe',
)


TEMPLATE_DIRS = ()


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
)


# APPS SETTINGS #########################################
# django.contrib.sites
SITE_ID = 1

# django.contrib.admin
ADMIN_MEDIA_PREFIX = '/static/admin/'

# django debug toolbar
INTERNAL_IPS = (
    '127.0.0.1',
)
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS' : False
}

# django.contrib.staticfiles
STATIC_ROOT = projectpath('static')
STATIC_URL = '/static/'

# media files
MEDIA_ROOT = projectpath('media')
MEDIA_URL = '/media/'
# APPS SETTINGS #########################################

