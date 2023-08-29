from .common import *
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = ["localhost"]

DATABASES = {
    'default': dj_database_url.config()
}