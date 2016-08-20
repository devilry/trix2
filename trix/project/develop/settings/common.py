"""
Common development settings.
"""
from trix.project.default.settings import *

DEBUG = True
TEMPLATE_DEBUG = True
ROOT_URLCONF = 'trix.project.develop.urls'

INSTALLED_APPS = list(INSTALLED_APPS) + [
    'django_dbdev',
    # 'debug_toolbar',
]

from django_dbdev.backends.postgres import DBSETTINGS

DATABASES = {
    'default': DBSETTINGS
}
DATABASES['default']['PORT'] = 20987
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MIDDLEWARE_CLASSES += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
