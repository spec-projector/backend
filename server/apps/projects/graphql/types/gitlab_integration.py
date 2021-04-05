from apps.projects.graphql.types.base import BaseIntegrationType


class GitLabIntegrationType(BaseIntegrationType):
    """GitLabIntegration type."""

    class Meta:
        name = "GitLabIntegration"
