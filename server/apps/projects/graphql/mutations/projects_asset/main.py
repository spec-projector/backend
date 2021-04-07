from apps.projects.graphql.mutations.projects_asset import create


class ProjectsAssetsMutations:
    """All projects assets mutations."""

    upload_figma_asset = create.CreateProjectAssetMutation.Field()
