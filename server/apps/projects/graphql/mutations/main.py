from apps.projects.graphql.mutations import projects, projects_assets


class ProjectsMutations(
    projects.ProjectsMutations,
    projects_assets.ProjectsAssetsMutations,
):
    """All projects mutations."""
