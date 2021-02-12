import graphene

from apps.projects.graphql.types import ProjectType


class ProjectAssetType(graphene.ObjectType):
    """Project asset type."""

    class Meta:
        name = "ProjectAsset"

    project = graphene.Field(ProjectType)
    file = graphene.String()  # noqa: WPS110
    source = graphene.String()
