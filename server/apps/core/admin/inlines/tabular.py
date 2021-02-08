from django.contrib import admin
from jnt_admin_tools.mixins import AutocompleteFieldsAdminMixin

from apps.core.admin.mixins import AdminFormFieldsOverridesMixin


class BaseTabularInline(
    AutocompleteFieldsAdminMixin,
    AdminFormFieldsOverridesMixin,
    admin.TabularInline,
):
    """Base tabular inline."""

    extra = 0
    show_change_link = True
