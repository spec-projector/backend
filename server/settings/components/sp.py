# -*- coding: utf-8 -*-

from decouple import config

SP_APP_VERSION = config("APP_VERSION", default=None)
