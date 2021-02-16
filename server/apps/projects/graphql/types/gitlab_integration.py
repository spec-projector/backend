import graphene

from apps.projects.graphql.resolvers import resolve_token_integration


class GitLabIntegrationType(graphene.ObjectType):
    """GitLabIntegration type."""

    class Meta:
        name = "GitLabIntegration"

    token = graphene.String(required=True, resolver=resolve_token_integration)
