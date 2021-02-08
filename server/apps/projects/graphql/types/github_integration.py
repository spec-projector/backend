import graphene


class GitHubIntegrationType(graphene.ObjectType):
    """GitHubIntegration type."""

    class Meta:
        name = "GitHubIntegration"

    token = graphene.String(required=True)
