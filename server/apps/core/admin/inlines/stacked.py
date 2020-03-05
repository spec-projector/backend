# -*- coding: utf-8 -*-

from django.contrib import admin

from apps.core.admin.mixins import AdminFormFieldsOverridesMixin


class BaseStackedInline(AdminFormFieldsOverridesMixin, admin.StackedInline):
    """Base stacked inline."""

    extra = 0
    show_change_link = True
