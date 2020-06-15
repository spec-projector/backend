# -*- coding: utf-8 -*-

from jnt_django_toolbox.admin.widgets import BitFieldWidget
from jnt_django_toolbox.models.fields import BitField


class AdminFormFieldsOverridesMixin:
    """Form fields override mixin."""

    formfield_overrides = {
        BitField: {"widget": BitFieldWidget},
    }
