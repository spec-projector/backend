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
    for bit_number in range(len(flags)):  # noqa: WPS518
        bit_handler.set_bit(bit_number, true_or_false=True)

    return bit_handler
