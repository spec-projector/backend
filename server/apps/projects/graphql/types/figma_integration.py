import graphene

from apps.projects.graphql.resolvers import resolve_token_integration


class FigmaIntegrationType(graphene.ObjectType):
    """FigmaIntegration type."""

    class Meta:
        name = "FigmaIntegration"

    token = graphene.String(required=True, resolver=resolve_token_integration)
