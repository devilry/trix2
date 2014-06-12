"""
Common development settings.
"""
from trix.project.default.settings import *


DEBUG = True
TEMPLATE_DEBUG = True
ROOT_URLCONF = 'trix.project.develop.urls'

INSTALLED_APPS = list(INSTALLED_APPS) + [
    'django_dbdev',
    'django_extensions',
]


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'