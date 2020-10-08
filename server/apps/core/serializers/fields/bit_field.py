import json

from jnt_django_toolbox.models.fields.bit.types import BitHandler
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class BitField(serializers.ListField):
    """Bit field serializer."""

    def __init__(self, *args, **kwargs):
        """Initializing."""
        self.child = serializers.ChoiceField(choices=kwargs.pop("choices"))
        super().__init__(*args, **kwargs)

    def to_representation(self, flags):
        """Convert bitfield to human representation."""
        return [flag for flag, setted in flags if setted]

    def to_internal_value(self, source) -> int:
        """Convert bitfield to internal representation."""
        source = json.loads(source) if isinstance(source, str) else source

        if not source:
            return 0

        bit_handler = BitHandler(0, list(self.child.choices))
        for flag in source:
            try:
                setattr(bit_handler, str(flag), True)  # noqa: WPS425
            except AttributeError:
                raise ValidationError("Unknown choice: {0}".format(flag))
        return int(bit_handler)
