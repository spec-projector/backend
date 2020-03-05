# -*- coding: utf-8 -*-

from admin_tools.mixins import AdminAutocompleteFieldsMixin
from django.contrib import admin

from apps.core.admin.base import BaseModelAdmin
from apps.projects.admin.filters import OwnerAutocompleteFilter
from apps.projects.admin.inlines import ProjectMemberInline
from apps.projects.models import Project


@admin.register(Project)
class ProjectAdmin(AdminAutocompleteFieldsMixin, BaseModelAdmin):
    """Project admin."""

    list_display = ("title", "owner", "created_at", "public")
    search_fields = ("title",)
    list_filter = (OwnerAutocompleteFilter, "public")
    inlines = (ProjectMemberInline,)
