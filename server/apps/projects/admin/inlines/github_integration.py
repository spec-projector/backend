from apps.core.admin.inlines import BaseTabularInline
from apps.projects.models import GitHubIntegration


class GitHubIntegrationInline(BaseTabularInline):
    """GitHub integration inline."""

    model = GitHubIntegration
