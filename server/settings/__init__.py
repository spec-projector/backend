from os import environ

from split_settings.tools import include

ENV = environ.get('DJANGO_ENV') or 'development'

# raise Exception(f'HERE!!! {ENV}')

include(
    'components/*.py',
    'environments/{0}.py'.format(ENV),
)
