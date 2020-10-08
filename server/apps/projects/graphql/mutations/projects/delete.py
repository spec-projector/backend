from typing import Dict, Optional

import graphene
from graphql import ResolveInfo
from jnt_django_graphene_toolbox.mutations import SerializerMutation

from apps.projects.graphql.mutations.projects.inputs import DeleteProjectInput
from apps.projects.models import Project


class DeleteProjectMutation(SerializerMutation):
    """Delete project mutation."""

    class Meta:
        serializer_class = DeleteProjectInput

    status = graphene.String()

    @classmethod
    def perform_mutate(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        validated_data: Dict[str, Project],
    ) -> "DeleteProjectMutation":
        """Perform mutation."""
        validated_data["project"].delete()

        return cls(status="success")
