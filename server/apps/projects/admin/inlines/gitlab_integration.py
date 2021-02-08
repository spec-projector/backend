from apps.core.admin.inlines import BaseTabularInline
from apps.projects.models import GitLabIntegration


class GitLabIntegrationInline(BaseTabularInline):
    """GitLab integration inline."""

    model = GitLabIntegration
