import os
from .common import *
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = []

DATABASES = {
    'default': dj_database_url.config()
}