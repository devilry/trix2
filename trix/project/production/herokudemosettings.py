"""
Settings for the Heroku demo.
"""
from .settings import *     # noqa
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
