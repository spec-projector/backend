import graphene

from apps.core.utils.media import get_absolute_path
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
        return get_absolute_path(self.file)
