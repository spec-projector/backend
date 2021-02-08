from django.contrib import admin

from apps.core.admin.base import BaseModelAdmin
from apps.core.services.couchdb import delete_couch_databases
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

    def delete_queryset(self, request, queryset):
        """Delete queryset."""
        db_names = list(queryset.values_list("db_name", flat=True))
        super().delete_queryset(request, queryset)
        delete_couch_databases(db_names)
