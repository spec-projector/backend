import graphene
from django.db import models
from graphql import ResolveInfo
from jnt_django_graphene_toolbox import fields, types

from apps.core.logic import queries
from apps.media.graphql.types import ImageType
from apps.projects.graphql.types import (
    FigmaIntegrationType,
    GitHubIntegrationType,
    GitLabIntegrationType,
    ProjectMemberType,
    ProjectMeType,
)
from apps.projects.logic.queries.project import allowed, project_me
from apps.projects.logic.queries.project_member import active
from apps.projects.models import Project, enums
from apps.users.graphql.types import UserType


class ProjectType(types.BaseModelObjectType):
    """Project type."""

    class Meta:
        model = Project

    is_public = graphene.Boolean()
    title = graphene.String()
    description = graphene.String()
    db_name = graphene.String()
    owner = graphene.Field(UserType)
    members = graphene.List(ProjectMemberType)
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()
    figma_integration = graphene.Field(FigmaIntegrationType)
    github_integration = graphene.Field(GitHubIntegrationType)
    gitlab_integration = graphene.Field(GitLabIntegrationType)
    emblem = graphene.Field(ImageType)
    public_role = graphene.Enum.from_enum(enums.ProjectMemberRole)()
    public_permissions = fields.BitField(enums.ProjectPermission)
    me = graphene.Field(ProjectMeType)

    @classmethod
    def get_queryset(
        cls,
        queryset: models.QuerySet,
        info: ResolveInfo,  # noqa: WPS110
    ) -> models.QuerySet:
        """Get queryset."""
        return queries.execute_query(
            allowed.Query(
                user=info.context.user,  # type: ignore
                queryset=queryset,
                include_public=True,
            ),
        )

    def resolve_members(
        self: Project,
        info: ResolveInfo,  # noqa: WPS110
    ) -> models.QuerySet:
        """Resolves project members."""
        return queries.execute_query(
            active.Query(
                project=self,
            ),
        )

    def resolve_me(
        self: Project,
        info: ResolveInfo,  # noqa: WPS110
    ) -> project_me.ProjectMe:
        """Resolve me project."""
        user = info.context.user  # type: ignore
        return queries.execute_query(
            project_me.Query(
                user=user if user.is_authenticated else None,
                project=self,
            ),
        )
