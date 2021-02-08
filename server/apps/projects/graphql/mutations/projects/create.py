from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseUseCaseMutation
from apps.projects.graphql.mutations.projects.inputs import BaseProjectInput
from apps.projects.graphql.types.project import ProjectType
from apps.projects.use_cases.project import create as project_create


class CreateProjectInput(BaseProjectInput):
    """Input for create project."""

    title = graphene.String(required=True)


class CreateProjectMutation(BaseUseCaseMutation):
    """Create project mutation."""

    class Meta:
        use_case_class = project_create.UseCase
        auth_required = True

    class Arguments:
        input = graphene.Argument(CreateProjectInput)  # noqa: WPS125

    project = graphene.Field(ProjectType)

    @classmethod
    def get_input_dto(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ):
        """Prepare use case input data."""
        return project_create.InputDto(
            user=info.context.user,  # type: ignore
            data=project_create.ProjectDto(**kwargs.get("input")),
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        output_dto: project_create.OutputDto,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {
            "project": output_dto.project,
        }
