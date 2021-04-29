import graphene
from django.db import models
from graphql import ResolveInfo

from apps.core.graphql.fields import BaseQueryConnectionField
from apps.core.logic.queries import IQuery
from apps.projects.graphql.types import ProjectType
from apps.projects.logic.queries.project import allowed


class ProjectConnectionField(BaseQueryConnectionField):
    """Handler for projects collections."""

    query = allowed.ListAllowedProjectsQuery
    auth_required = True

    def __init__(self):
        """Initialize."""
        super().__init__(
            ProjectType,
            title=graphene.String(),
        )

    @classmethod
    def build_query(
        cls,
        queryset: models.QuerySet,
        info: ResolveInfo,  # noqa: WPS110
        args,
    ) -> IQuery:
        """Prepare query input data."""
        return cls.query(
            queryset=queryset,
            filters=allowed.ProjectFilter(
                title=args.get("title"),
            ),
            sort=args.get("sort"),
            user=info.context.user,  # type: ignore
        )
