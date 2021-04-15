import graphene

from apps.core.utils.images import generate_file_path
from apps.projects.graphql.types import ProjectType


class ProjectAssetType(graphene.ObjectType):
    """Project asset type."""

    class Meta:
        name = "ProjectAsset"

    project = graphene.Field(ProjectType)
    file = graphene.String()  # noqa: WPS110
    source = graphene.String()
    file_url = graphene.String()

    def resolve_file(self, info):  # noqa: WPS110
        """Resolve file absolute path."""
        return generate_file_path(self.file, info.context)
