import graphene
from jnt_django_graphene_toolbox.fields import BaseModelConnectionField
from jnt_django_graphene_toolbox.filters import SortHandler

from apps.projects.graphql.fields.filters import ProjectsFilterSet
from apps.projects.graphql.types import ProjectType


class ProjectSort(graphene.Enum):
    """Allowed sort fields."""

    CREATED_AT_ASC = "created_at"  # noqa: WPS115
    CREATED_AT_DESC = "-created_at"  # noqa: WPS115


class ProjectConnectionField(BaseModelConnectionField):
    """Handler for projects collections."""

    filterset_class = ProjectsFilterSet
    auth_required = True
    sort_handler = SortHandler(ProjectSort)

    def __init__(self):
        """Initialize."""
        super().__init__(
            ProjectType,
            title=graphene.String(),
        )
