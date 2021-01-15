from typing import Dict, Optional

import graphene
from graphql import ResolveInfo
from jnt_django_graphene_toolbox.fields import BitField

from apps.core.graphql.mutations import BaseUseCaseMutation
from apps.core.utils.objects import empty
from apps.projects.graphql.types.project import ProjectType
from apps.projects.use_cases.project import update as project_update


class ProjectMemberInput(graphene.InputObjectType):
    """Project member input type."""

    id = graphene.ID(required=True)  # noqa: A003, WPS125
    roles = BitField(required=True)


class UpdateProjectMutation(BaseUseCaseMutation):
    """Update project mutation."""

    class Meta:
        use_case_class = project_update.UseCase
        auth_required = True

    class Arguments:
        id = graphene.ID(required=True)  # noqa: A003, WPS125
        title = graphene.String()
        is_public = graphene.Boolean()
        description = graphene.String()
        users = graphene.Argument(graphene.List(ProjectMemberInput))

    project = graphene.Field(ProjectType)

    @classmethod
    def get_input_dto(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ):
        """Prepare use case input data."""
        return project_update.InputDto(
            user=info.context.user,  # type: ignore
            data=project_update.ProjectUpdateData(
                project=kwargs["id"],
                title=kwargs.get("title", empty),
                is_public=kwargs.get("is_public", empty),
                description=kwargs.get("description", empty),
                users=kwargs.get("users", empty),
            ),
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        output_dto: project_update.OutputDto,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {
            "project": output_dto.project,
        }
