from typing import Dict, Optional

import graphene
from graphql import ResolveInfo
from jnt_django_graphene_toolbox.mutations import SerializerMutation

from apps.projects.graphql.mutations.projects.inputs import CreateProjectInput
from apps.projects.graphql.types.project import ProjectType
from apps.projects.models.project import Project


class CreateProjectMutation(SerializerMutation):
    """Create project mutation."""

    class Meta:
        serializer_class = CreateProjectInput

    project = graphene.Field(ProjectType)

    @classmethod
    def perform_mutate(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        validated_data: Dict[str, str],
    ) -> "CreateProjectMutation":
        """Perform mutation."""
        project = Project.objects.create(
            title=validated_data["title"],
            owner=info.context.user,  # type: ignore
        )

        return cls(project=project)
