# -*- coding: utf-8 -*-

from django.contrib.contenttypes.admin import GenericTabularInline

from apps.core.admin.mixins import AdminFormFieldsOverridesMixin


class BaseGenericTabularInline(
    AdminFormFieldsOverridesMixin, GenericTabularInline,
):
    """Base generic tabular inline."""

    extra = 0
    show_change_link = True
