from .common import *

DEBUG = True

MIDDLEWARE += ['silk.middleware.SilkyMiddleware']

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.mysql",
        "HOST": os.environ.get("DB_HOST"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
        "PORT": os.environ.get("DB_PORT"),
    }
}

# Loading env vars from .env file for testing
if os.environ.get("TEST_MODE") in [None, "", "true", "1"]:
    from decouple import config
    DATABASES = {
        'default': {
            "ENGINE": "django.db.backends.mysql",
            "HOST": config("TEST_DB_HOST"),
            "NAME": config("DB_NAME"),
            "USER": config("TEST_DB_USER"),
            "PASSWORD": config("DB_ROOT_PASS"),
            "PORT": config("DB_PORT"),
        }
    }

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
}
