import graphene

from apps.projects.graphql.resolvers import resolve_token_integration


class GitHubIntegrationType(graphene.ObjectType):
    """GitHubIntegration type."""

    class Meta:
        name = "GitHubIntegration"

    token = graphene.String(required=True, resolver=resolve_token_integration)
