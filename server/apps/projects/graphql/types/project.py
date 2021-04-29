import graphene
from django.db.models import QuerySet
from graphql import ResolveInfo
from jnt_django_graphene_toolbox.types import BaseModelObjectType

from apps.core.logic import queries
from apps.projects.graphql.types import (
    FigmaIntegrationType,
    GitHubIntegrationType,
    GitLabIntegrationType,
)
from apps.projects.graphql.types.project_member import ProjectMemberType
from apps.projects.logic.queries.project import allowed
from apps.projects.logic.queries.project_member import active
from apps.projects.models import Project
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
    members = graphene.List(ProjectMemberType)
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()
    figma_integration = graphene.Field(FigmaIntegrationType)
    github_integration = graphene.Field(GitHubIntegrationType)
    gitlab_integration = graphene.Field(GitLabIntegrationType)

    @classmethod
    def get_queryset(
        cls,
        queryset: QuerySet,
        info: ResolveInfo,  # noqa: WPS110
    ) -> QuerySet:
        """Get queryset."""
        return queries.execute_query(
            allowed.ListAllowedProjectsQuery(
                user=info.context.user,  # type: ignore
                queryset=queryset,
                include_public=True,
            ),
        )

    def resolve_members(
        self: Project,
        info: ResolveInfo,  # noqa: WPS110
    ) -> QuerySet:
        """Resolves project members."""
        return queries.execute_query(
            active.ListActiveProjectMembersQuery(
                project=self,
            ),
        )
