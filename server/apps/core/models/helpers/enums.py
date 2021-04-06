from typing import Type

from django.db import models


def max_enum_len(enum_class: Type[models.Choices]) -> int:
    """Calculate max choice value length."""
    return len(max(enum_class.values, key=len))
