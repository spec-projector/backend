from apps.projects.graphql.types.base import BaseIntegrationType


class GitHubIntegrationType(BaseIntegrationType):
    """GitHubIntegration type."""

    class Meta:
        name = "GitHubIntegration"
