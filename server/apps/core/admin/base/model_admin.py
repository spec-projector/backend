from django.contrib import admin
from jnt_admin_tools.mixins.autocomplete import AutocompleteAdminMixin

from apps.core.admin.mixins import AdminFormFieldsOverridesMixin


class BaseModelAdmin(
    AutocompleteAdminMixin,
    AdminFormFieldsOverridesMixin,
    admin.ModelAdmin,
):
    """Base model admin."""

    class Media:
        """Media."""

    list_per_page = 20
