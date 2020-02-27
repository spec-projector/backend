# -*- coding: utf-8 -*-

import graphene
from django.db.models import QuerySet
from graphql import ResolveInfo

from apps.core.graphql.connections import DataSourceConnection
from apps.core.graphql.relay_nodes import DatasourceRelayNode
from apps.core.graphql.types import BaseDjangoObjectType
from apps.projects.graphql.resolvers import resolve_project_members
from apps.projects.graphql.types.project_member import ProjectMemberType
from apps.projects.models import Project, ProjectMember


class ProjectType(BaseDjangoObjectType):
    members = graphene.List(
        ProjectMemberType,
        resolver=resolve_project_members,
    )

    class Meta:
        model = Project
        interfaces = (DatasourceRelayNode,)
        connection_class = DataSourceConnection
        name = "Project"

    @classmethod
    def get_queryset(
        cls,
        queryset: QuerySet,
        info: ResolveInfo,  # noqa: WPS110
    ) -> QuerySet:
        """Get queryset."""
        # TODO: override (must be 1 queryset)
        project_ids = ProjectMember.objects.filter(
            user=info.context.user,
            roles__gt=0,
        ).values_list(
            "project_id",
            flat=True,
        )

        project_owner_ids = queryset.filter(
            owner=info.context.user,
        ).values_list(
            "id",
            flat=True,
        )

        return queryset.filter(id__in={*project_ids, *project_owner_ids})
