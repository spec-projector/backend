# -*- coding: utf-8 -*-

import sentry_sdk
from decouple import config
from graphql import GraphQLError
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

from settings.components.sp import SP_APP_VERSION

STANDARD_FORMAT = "[%(asctime)s]|%(levelname)s|%(module)s.%(funcName)s:%(lineno)s|%(message)s"  # noqa: E501, WPS323

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": STANDARD_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",  # noqa: WPS323
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}


def _before_send_sentry_handler(event, hint):
    exc_info = hint.get("exc_info")
    if exc_info:
        exc_type, exc_value, tb = exc_info
        if isinstance(exc_value, GraphQLError):
            return None

    return event


sentry_dsn = config("DJANGO_SENTRY_DSN", default=None)
if sentry_dsn:
    sentry_sdk.init(  # type:ignore
        dsn=sentry_dsn,
        release=SP_APP_VERSION,
        integrations=[DjangoIntegration(), CeleryIntegration()],
        send_default_pii=True,
        before_send=_before_send_sentry_handler,
    )
    sentry_sdk.utils.MAX_STRING_LENGTH = 4096
