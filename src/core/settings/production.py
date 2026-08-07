import os
import dj_database_url


SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = True if os.environ.get('DEBUG', 'False') == 'True' else False

DEFAULT_CONNECTION = dj_database_url.parse(os.environ.get('DATABASE_URL'))
DEFAULT_CONNECTION.update({'CONN_MAX_AGE': 600})
DATABASES = {
    'default': DEFAULT_CONNECTION
}

CORS_ALLOWED_ORIGINS = []