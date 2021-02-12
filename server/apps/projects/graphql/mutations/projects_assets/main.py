from apps.projects.graphql.mutations.projects_assets import create


class ProjectsAssetsMutations:
    """All projects assets mutations."""

    upload_figma_asset = create.CreateProjectAssetMutation.Field()
