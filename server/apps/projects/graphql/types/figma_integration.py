import graphene


class FigmaIntegrationType(graphene.ObjectType):
    """FigmaIntegration type."""

    class Meta:
        name = "FigmaIntegration"

    token = graphene.String(required=True)
