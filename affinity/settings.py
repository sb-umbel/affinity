from dj_database_url import config as dbconfig
from getenv import env
from os.path import abspath, dirname


BASE_DIR = dirname(dirname(abspath(__file__)))

SECRET_KEY = env('SECRET_KEY', required=True)
DEBUG = env('DEBUG', required=True)

ALLOWED_HOSTS = [
    '127.0.0.1',
    'affinitysb.herokuapp.com',
]

INSTALLED_APPS = [
    'affinity.apps.AffinityConfig',
]

MIDDLEWARE_CLASSES = []

ROOT_URLCONF = 'affinity.urls'

WSGI_APPLICATION = 'affinity.wsgi.application'

DATABASES = {
    'default': dbconfig(env='DATABASE_URL'),
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
USE_TZ = True

USE_I18N = False
USE_L10N = False

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
