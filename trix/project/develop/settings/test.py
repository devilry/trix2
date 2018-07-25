from .common import *           # noqa

# We test against the english original text
LANGUAGE_CODE = 'en'

# Faster tests with less time spent on hashing passwords
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
)

COMPRESS_ENABLED = False
