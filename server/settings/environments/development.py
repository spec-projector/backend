# -*- coding: utf-8 -*-

from server import BASE_DIR

DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'spec_projector',
        'USER': 'admin',
        'PASSWORD': '229835',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

CELERY_TASK_ALWAYS_EAGER = True

STATIC_ROOT = BASE_DIR.joinpath('static')

SECRET_KEY = 'dev'
