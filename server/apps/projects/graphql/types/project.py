import graphene
from django.db.models import QuerySet
from graphql import ResolveInfo
from jnt_django_graphene_toolbox.types import BaseModelObjectType

from apps.projects.graphql.resolvers import resolve_project_members
from apps.projects.graphql.types.project_member import ProjectMemberType
from apps.projects.models import Project
from apps.projects.services.projects.available_projects import (
    get_available_projects,
)
from apps.users.graphql.types import UserType


class ProjectType(BaseModelObjectType):
    """Project type."""

    class Meta:
        model = Project

    is_public = graphene.Boolean()
    title = graphene.String()
    description = graphene.String()
    db_name = graphene.String()
    owner = graphene.Field(UserType)
    members = graphene.List(
        ProjectMemberType,
        resolver=resolve_project_members,
    )
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()

    @classmethod
    def get_queryset(
        cls,
        queryset: QuerySet,
        info: ResolveInfo,  # noqa: WPS110
    ) -> QuerySet:
        """Get queryset."""
        return cls._get_queryset(queryset, info)

    @classmethod
    def _get_queryset(
        cls,
        queryset: QuerySet,
        info: ResolveInfo,  # noqa: WPS110
    ) -> QuerySet:
        user = info.context.user  # type: ignore

        return get_available_projects(queryset, user)
