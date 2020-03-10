# -*- coding: utf-8 -*-

from django.contrib.contenttypes.admin import GenericStackedInline

from apps.core.admin.mixins import AdminFormFieldsOverridesMixin


class BaseGenericStackedInline(
    AdminFormFieldsOverridesMixin, GenericStackedInline,
):
    """Base generic stacked inline."""

    extra = 0
    show_change_link = True
