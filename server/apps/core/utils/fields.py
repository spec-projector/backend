from django.db import models
from jnt_django_toolbox.models.fields.bit.types import Bit, BitHandler


def get_all_selected_bitfield(flags: models.TextChoices) -> BitHandler:
    """Get all selected bitfield."""
    flags_keys = []
    flags_labels = []
    for flag_key, flag_label in flags.choices:
        flags_keys.append(flag_key)
        flags_labels.append(flag_label)

    return BitHandler(_get_internal_value(flags), flags_keys, flags_labels)


def _get_internal_value(flags: models.TextChoices) -> int:
    """Get internal value."""
    internal_value = 0
    for index, _ in enumerate(flags):
        internal_value |= Bit(index)

    return internal_value
