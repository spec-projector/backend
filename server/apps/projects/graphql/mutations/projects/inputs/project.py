import graphene


class UpdateFigmaIntegrationType(graphene.InputObjectType):
    """FigmaIntegration type."""

    token = graphene.String(required=True)


class UpdateGitHubIntegrationType(graphene.InputObjectType):
    """GitHubIntegration type."""

    token = graphene.String(required=True)


class UpdateGitLabIntegrationType(graphene.InputObjectType):
    """GitLabIntegration type."""

    token = graphene.String(required=True)


class BaseProjectInput(graphene.InputObjectType):
    """Input for updating profile."""

    is_public = graphene.Boolean()
    description = graphene.String()
    figma_integration = graphene.Field(UpdateFigmaIntegrationType)
    github_integration = graphene.Field(UpdateGitHubIntegrationType)
    gitlab_integration = graphene.Field(UpdateGitLabIntegrationType)
