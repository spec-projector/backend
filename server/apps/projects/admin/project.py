from django.contrib import admin

from apps.core.admin.base import BaseModelAdmin
from apps.projects.admin.filters import OwnerAutocompleteFilter
from apps.projects.admin.inlines import (
    FigmaIntegrationInline,
    GitHubIntegrationInline,
    GitLabIntegrationInline,
    ProjectMemberInline,
)
from apps.projects.models import Project


@admin.register(Project)
class ProjectAdmin(BaseModelAdmin):
    """Project admin."""

    list_display = ("title", "id", "owner", "created_at", "is_public")
    search_fields = ("title",)
    list_filter = (OwnerAutocompleteFilter, "is_public")
    inlines = (
        ProjectMemberInline,
        FigmaIntegrationInline,
        GitHubIntegrationInline,
        GitLabIntegrationInline,
    )
