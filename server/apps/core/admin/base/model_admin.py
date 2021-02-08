from django.contrib import admin
from jnt_admin_tools.mixins import AutocompleteFieldsAdminMixin

from apps.core.admin.mixins import AdminFormFieldsOverridesMixin


class BaseModelAdmin(
    AutocompleteFieldsAdminMixin,
    AdminFormFieldsOverridesMixin,
    admin.ModelAdmin,
):
    """Base model admin."""

    class Media:
        """Media."""

    list_per_page = 20
