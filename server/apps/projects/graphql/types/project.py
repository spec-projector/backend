import graphene
from django.db.models import QuerySet
from graphql import ResolveInfo
from jnt_django_graphene_toolbox.types import BaseModelObjectType

from apps.projects.graphql.resolvers import resolve_project_members
from apps.projects.graphql.types.project_member import ProjectMemberType
from apps.projects.models import Project, ProjectMember
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
        user = info.context.user
        if user.is_anonymous:  # type: ignore
            return cls._get_queryset_for_anonymous(queryset)

        # TODO: override (must be 1 queryset)
        public_project_ids = queryset.filter(
            is_public=True,
        ).values_list("id", flat=True)

        project_ids = ProjectMember.objects.filter(
            user_id=info.context.user.id,  # type: ignore
            roles__gt=0,
        ).values_list("project_id", flat=True)

        project_owner_ids = queryset.filter(
            owner_id=info.context.user.id,  # type: ignore
        ).values_list("id", flat=True)

        return queryset.filter(
            id__in={*project_ids, *project_owner_ids, *public_project_ids},
        )

    @classmethod
    def _get_queryset_for_anonymous(cls, queryset: QuerySet) -> QuerySet:
        return queryset.filter(is_public=True)
