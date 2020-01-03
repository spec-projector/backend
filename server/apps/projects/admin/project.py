# -*- coding: utf-8 -*-

from admin_tools.mixins import AdminAutocompleteFieldsMixin
from django.contrib import admin

from apps.core.admin.base import BaseModelAdmin
from apps.projects.admin.filters import OwnerAutocompleteFilter
from apps.projects.models import Project


@admin.register(Project)
class ProjectAdmin(AdminAutocompleteFieldsMixin, BaseModelAdmin):
    list_display = ("title", "owner", "created_at")
    search_fields = ("title",)
    list_filter = (OwnerAutocompleteFilter,)
