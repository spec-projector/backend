from server import BASE_DIR

DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'spec_projector',
        'USER': 'postgres',
        'PASSWORD': 'pass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

CELERY_TASK_ALWAYS_EAGER = True

STATIC_ROOT = BASE_DIR.joinpath('static')

SECRET_KEY = 'dev'


SOCIAL_AUTH_GITLAB_KEY = 'd49b427ea4363d11ebe74f72102e2519d25460c888f20739b4240bab7b960d95'
SOCIAL_AUTH_GITLAB_SECRET = '278233e131428a7bfff5caabbb985d559a16135a6b2e1b09faa0321dbf79ef4c'
SOCIAL_AUTH_GITLAB_REDIRECT_URI = 'http://127.0.0.1:8000/api/complete/gitlab'