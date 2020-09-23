# -*- coding: utf-8 -*-

import sentry_sdk
from decouple import config
from graphql import GraphQLError
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

# graphene wtf!!!
IGNORED_ERRORS_TXT = ("graphql.error.located_error.GraphQLLocatedError",)


def _before_send_sentry_handler(event, hint):
    exc_info = hint.get("exc_info")
    if exc_info:
        _, exc_value, tb = exc_info
        if isinstance(exc_value, GraphQLError):
            return None
    else:
        log_record = hint.get("log_record")
        skip_event = log_record and any(
            err in log_record.message for err in IGNORED_ERRORS_TXT
        )
        if skip_event:
            return None
    return event


sentry_dsn = config("DJANGO_SENTRY_DSN", default=None)
if sentry_dsn:
    sentry_sdk.init(  # type:ignore
        dsn=sentry_dsn,
        release=SP_APP_VERSION,
        integrations=[DjangoIntegration()],
        send_default_pii=True,
        before_send=_before_send_sentry_handler,
        ignore_errors=[GraphQLError],
    )
    sentry_sdk.utils.MAX_STRING_LENGTH = 4096
