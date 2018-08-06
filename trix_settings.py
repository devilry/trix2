from trix.project.production.settings import *
import dj_database_url

# Make this 50 chars and RANDOM - do not share it with anyone
SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# Database config
DATABASE_URL = 'sqlite:///db.sqlite3'
DATABASES = {'default': dj_database_url.config(default=DATABASE_URL)}

# Set this to False to turn of debug mode in production
DEBUG = False
