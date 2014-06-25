import os
# import urlparse
import dj_database_url

from trix.project.default.settings import *


ROOT_URLCONF = 'trix.project.production.urls'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Database
DATABASES = {}
DATABASES['default'] = dj_database_url.config()

# Cache with https://addons.heroku.com/memcachedcloud
# redis_url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
# CACHES = {
#     'default': {
#         'BACKEND': 'redis_cache.RedisCache',
#         'LOCATION': '{hostname}:{port}'.format(
#             hostname=redis_url.hostname, port=redis_url.port),
#         'OPTIONS': {
#             'PASSWORD': redis_url.password,
#             'DB': 0,
#         }
#     }
# }

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration for heroku
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
#         'URL': os.environ['SEARCHBOX_URL'],
#         'INDEX_NAME': 'documents',
#     },
# }


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s %(asctime)s %(name)s %(pathname)s:%(lineno)s] %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'stderr': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['stderr'],
            'level': 'INFO',
            'propagate': False
        },
        'django.db': {
            'handlers': ['stderr'],
            'level': 'INFO',
            'propagate': False
        },
        '': {
            'handlers': ['stderr'],
            'level': 'INFO',
            'propagate': False
        }
    }
}
