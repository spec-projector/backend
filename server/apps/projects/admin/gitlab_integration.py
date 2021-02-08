from django.contrib import admin

from apps.core.admin.base import BaseModelAdmin
from apps.projects.models import GitLabIntegration


@admin.register(GitLabIntegration)
class GitLabIntegrationAdmin(BaseModelAdmin):
    """GitHub integration admin."""

    search_fields = ("id",)
