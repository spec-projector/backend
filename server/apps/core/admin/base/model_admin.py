# -*- coding: utf-8 -*-

from django.contrib import admin

from apps.core.admin.mixins import AdminFormFieldsOverridesMixin


class BaseModelAdmin(AdminFormFieldsOverridesMixin, admin.ModelAdmin):
    list_per_page = 20

    class Media:
        """Media."""
