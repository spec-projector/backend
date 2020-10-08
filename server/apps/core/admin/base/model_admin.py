from django.contrib import admin

from apps.core.admin.mixins import AdminFormFieldsOverridesMixin


class BaseModelAdmin(AdminFormFieldsOverridesMixin, admin.ModelAdmin):
    """Base model admin."""

    class Media:
        """Media."""

    list_per_page = 20
