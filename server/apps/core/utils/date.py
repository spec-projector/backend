# -*- coding: utf-8 -*-

SECONDS_IN_MINUTE = 60
SECONDS_IN_HOUR = SECONDS_IN_MINUTE * 60


def seconds_to_hours(seconds: int) -> float:
    return round(seconds / SECONDS_IN_HOUR, 2)
