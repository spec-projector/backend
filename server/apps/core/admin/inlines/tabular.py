from django.contrib import admin

from apps.core.admin.mixins import AdminFormFieldsOverridesMixin


class BaseTabularInline(AdminFormFieldsOverridesMixin, admin.TabularInline):
    extra = 0
    show_change_link = True
