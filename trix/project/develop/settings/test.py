from .common import *

# We test against the english original text
LANGUAGE_CODE = 'en'

# South
SOUTH_TESTS_MIGRATE = False # To disable migrations and use syncdb instead
SKIP_SOUTH_TESTS = True # To disable South's own unit tests


# Faster tests with less time spent on hashing passwords
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
)

COMPRESS_ENABLED = False