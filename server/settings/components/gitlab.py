from decouple import config

GITLAB_HOST = config("DJANGO_GITLAB_HOST", default="https://gitlab.com")
