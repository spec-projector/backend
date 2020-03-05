# -*- coding: utf-8 -*-

from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple


class AdminFormFieldsOverridesMixin:
    """Form fields override mixin."""

    formfield_overrides = {
        BitField: {"widget": BitFieldCheckboxSelectMultiple},
    }
