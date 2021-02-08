import graphene


class GitLabIntegrationType(graphene.ObjectType):
    """GitLabIntegration type."""

    class Meta:
        name = "GitLabIntegration"

    token = graphene.String(required=True)
