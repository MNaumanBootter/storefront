"""
Django settings for storefront project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
from datetime import timedelta
from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+r0xtyf%n311!z4m60@fjl5(w(en1%chpczggp225^c#bc6kpi'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'corsheaders',
    'rest_framework',
    'djoser',
    'silk',
    'debug_toolbar',
    'store',
    'tags',
    'likes',
    'core',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE += ['silk.middleware.SilkyMiddleware']

CORS_ALLOWED_ORIGINS = []

ROOT_URLCONF = 'storefront.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'storefront.wsgi.application'


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


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
}

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'PAGE_SIZE': 10,
    # "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
}

AUTH_USER_MODEL = "core.User"


DJOSER = {
    "SERIALIZERS": {
        "user_create": "core.serializers.UserCreateSerializer",
        'current_user': 'core.serializers.UserSerializer',
    },
}


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp4dev"
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_HOST_PORT = int(os.environ.get('SMTP4DEV_PORT'))
DEFAULT_FOR_EMAIL = "from@example.com"

ADMINS = [
    ("Admin1", "admin1@example.com"),
    ("Admin2", "admin2@example.com"),
]

CELERY_BROKER_URL = (
    f"redis://{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}/1"
)

# CELERY_BEAT_SCHEDULE = {
#     "email_customers": {
#         "task": "store.tasks.email_customers",
#         # "schedule": crontab(minute="*/1"),
#         "schedule": 5,
#         # "args": ["hello"],
#         # "kwargs": {"a": "a"},
#     }
# }

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}/2",
        "TIMEOUT": 10 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "general.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": [
                "console",
                "file",
            ],
            "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO"),
        },
    },
    "formatters": {
        "verbose": {
            "format": "{asctime} ({levelname}) - {name} - {message}",
            "style": "{",
        }
    },
}
