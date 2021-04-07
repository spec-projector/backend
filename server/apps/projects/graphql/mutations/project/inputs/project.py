import graphene


class UpdateFigmaIntegrationType(graphene.InputObjectType):
    """FigmaIntegration type."""

    token = graphene.String(required=False)


class UpdateGitHubIntegrationType(graphene.InputObjectType):
    """GitHubIntegration type."""

    token = graphene.String(required=False)


class UpdateGitLabIntegrationType(graphene.InputObjectType):
    """GitLabIntegration type."""

    token = graphene.String(required=False)


class BaseProjectInput(graphene.InputObjectType):
    """Base input for add/create project."""

    title = graphene.String()
    is_public = graphene.Boolean()
    description = graphene.String()
    figma_integration = graphene.Field(UpdateFigmaIntegrationType)
    github_integration = graphene.Field(UpdateGitHubIntegrationType)
    gitlab_integration = graphene.Field(UpdateGitLabIntegrationType)
