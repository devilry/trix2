"""
Common development settings.
"""
from trix.project.default.settings import *             # noqa
from django_dbdev.backends.postgres import DBSETTINGS

DEBUG = True
ROOT_URLCONF = 'trix.project.develop.urls'

INSTALLED_APPS = list(INSTALLED_APPS) + [
    'django_dbdev',
    # 'debug_toolbar',
]

DATABASES = {
    'default': DBSETTINGS
}

DATABASES['default']['PORT'] = 20987

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# For testing collectstatic
STATIC_ROOT = 'staticfiles'
