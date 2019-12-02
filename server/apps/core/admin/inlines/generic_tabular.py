# -*- coding: utf-8 -*-

from django.contrib.contenttypes.admin import GenericTabularInline

from apps.core.admin.mixins import AdminFormFieldsOverridesMixin


class BaseGenericTabularInline(
    AdminFormFieldsOverridesMixin,
    GenericTabularInline,
):
    extra = 0
    show_change_link = True
