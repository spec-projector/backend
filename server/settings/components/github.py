from decouple import config

GITHUB_HOST = config("DJANGO_GITHUB_HOST", default="https://api.github.com")
