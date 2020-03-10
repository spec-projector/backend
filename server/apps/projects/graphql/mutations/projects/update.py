# -*- coding: utf-8 -*-

from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import SerializerMutation
from apps.core.graphql.mutations.helpers.persisters import (
    update_from_validated_data,
)
from apps.projects.graphql.mutations.projects.inputs import UpdateProjectInput
from apps.projects.graphql.types.project import ProjectType
from apps.projects.models import ProjectMember


class UpdateProjectMutation(SerializerMutation):
    """Update project mutation."""

    class Meta:
        serializer_class = UpdateProjectInput

    project = graphene.Field(ProjectType)

    @classmethod
    def perform_mutate(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110ø
        validated_data: Dict[str, object],
    ) -> "UpdateProjectMutation":
        """Perform mutation."""
        project = validated_data.pop("id")

        if "members" in validated_data:
            cls._update_members(project, validated_data.pop("members"))

        update_from_validated_data(project, validated_data)

        return cls(project=project)

    @classmethod
    def _update_members(cls, project, members) -> None:
        project_members = []
        for project_member_input in members:
            project_member, _ = ProjectMember.objects.update_or_create(
                project=project,
                user=project_member_input["user"],
                defaults={"roles": project_member_input.get("roles")},
            )

            project_members.append(project_member)

        for member in ProjectMember.objects.filter(project=project):
            if member not in project_members:
                member.delete()
