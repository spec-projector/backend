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
SOCIAL_AUTH_GITLAB_REDIRECT_URI = "https://{0}/signup/login".format(
    DOMAIN_NAME,
)
