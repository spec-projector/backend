import graphene
from django.db import models
from graphql import ResolveInfo

from apps.core.graphql.fields import BaseQueryConnectionField
from apps.projects.graphql.types import ProjectType
from apps.projects.logic.queries.project import allowed


class ProjectConnectionField(BaseQueryConnectionField):
    """Handler for projects collections."""

    query = allowed.Query
    auth_required = True

    def __init__(self):
        """Initialize."""
        super().__init__(
            ProjectType,
            title=graphene.String(),
        )

    @classmethod
    def get_input_dto(
        cls,
        queryset: models.QuerySet,
        info: ResolveInfo,  # noqa: WPS110
        args,
    ):
        """Prepare query input data."""
        return allowed.InputDto(
            queryset=queryset,
            filters=cls.get_filters_from_args(args, allowed.ProjectFilter),
            sort=cls.get_sort_from_args(args),
            user=info.context.user,
        )
