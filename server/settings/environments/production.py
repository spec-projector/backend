from decouple import config

SECRET_KEY = config("DJANGO_SECRET_KEY")
DOMAIN_NAME = config("DOMAIN_NAME")

ALLOWED_HOSTS = ["localhost", DOMAIN_NAME]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DJANGO_DATABASE_NAME"),
        "USER": config("DJANGO_DATABASE_USER"),
        "PASSWORD": config("DJANGO_DATABASE_PASSWORD"),
        "HOST": config("DJANGO_DATABASE_HOST"),
        "PORT": config("DJANGO_DATABASE_PORT", cast=int, default=5432),
        "CONN_MAX_AGE": config("CONN_MAX_AGE", cast=int, default=60),
    },
}

SOCIAL_AUTH_GITLAB_KEY = config("DJANGO_SOCIAL_AUTH_GITLAB_KEY")
SOCIAL_AUTH_GITLAB_SECRET = config("DJANGO_SOCIAL_AUTH_GITLAB_SECRET")
SOCIAL_AUTH_GITLAB_REDIRECT_URI = "https://{0}/oauth/gitlab".format(
    DOMAIN_NAME,
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config("DJANGO_SOCIAL_AUTH_GOOGLE_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config("DJANGO_SOCIAL_AUTH_GOOGLE_SECRET")
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = "https://{0}/oauth/google".format(
    DOMAIN_NAME,
)

CONSTANCE_DATABASE_CACHE_BACKEND = "default"

DEFAULT_FILE_STORAGE = "minio_storage.storage.MinioMediaStorage"

FLUENTD_HOST = config("DJANGO_FLUENTD", default=None)
if FLUENTD_HOST:
    LOGGING = {
        "version": 1,
        "formatters": {
            "fluentd": {
                "()": "fluent.handler.FluentRecordFormatter",
                "exclude_attrs": ("exc_info",),
            },
        },
        "handlers": {
            "fluentd": {
                "level": "DEBUG",
                "class": "fluent.handler.FluentHandler",
                "formatter": "fluentd",
                "tag": DOMAIN_NAME,
                "host": FLUENTD_HOST,
                "port": 24224,
            },
        },
        "loggers": {
            "django": {
                "handlers": ("fluentd",),
                "level": "WARNING",
                "propagate": False,
            },
            "apps": {
                "handlers": ("fluentd",),
                "level": "DEBUG",
                "propagate": False,
            },
            "celery": {
                "handlers": ("fluentd",),
                "level": "INFO",
                "propagate": False,
            },
        },
    }
