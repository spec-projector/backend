from django.contrib import admin

from apps.core.admin.mixins import AdminFormFieldsOverridesMixin


class BaseStackedInline(AdminFormFieldsOverridesMixin, admin.StackedInline):
    extra = 0
    show_change_link = True
