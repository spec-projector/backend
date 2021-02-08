from django.contrib import admin

from apps.core.admin.base import BaseModelAdmin
from apps.projects.models import GitHubIntegration


@admin.register(GitHubIntegration)
class GitHubIntegrationAdmin(BaseModelAdmin):
    """GitHub integration admin."""

    search_fields = ("id",)
