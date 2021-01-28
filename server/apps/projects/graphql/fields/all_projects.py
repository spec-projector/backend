import graphene
from jnt_django_graphene_toolbox.fields import BaseModelConnectionField

from apps.projects.graphql.fields.filters import ProjectsFilterSet
from apps.projects.graphql.types import ProjectType


class ProjectConnectionField(BaseModelConnectionField):
    """Handler for projects collections."""

    filterset_class = ProjectsFilterSet
    auth_required = True

    def __init__(self):
        """Initialize."""
        super().__init__(
            ProjectType,
            order_by=graphene.String(),
            title=graphene.String(),
        )
