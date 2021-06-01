from django.db import models
from jnt_django_toolbox.models.fields.bit.types import BitHandler


def get_all_selected_bitfield(flags: models.TextChoices) -> BitHandler:
    """Get all selected bitfield."""
    flags_as_dict = dict(flags.choices)
    bit_handler = BitHandler(
        0,
        list(flags_as_dict.keys()),
        list(flags_as_dict.values()),
    )

    for flag_key in flags_as_dict.keys():
        setattr(bit_handler, flag_key, True)

    return bit_handler
