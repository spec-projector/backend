from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseUseCaseMutation
from apps.projects.use_cases.project import delete as project_delete


class DeleteProjectMutation(BaseUseCaseMutation):
    """Delete project mutation."""

    class Meta:
        use_case_class = project_delete.UseCase
        auth_required = True

    class Arguments:
        project = graphene.ID(required=True)

    status = graphene.String()

    @classmethod
    def get_input_dto(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ):
        """Prepare use case input data."""
        return project_delete.InputDto(
            user=info.context.user,  # type: ignore
            data=project_delete.ProjectDeleteData(
                project=kwargs["project"],
            ),
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        output_dto,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {
            "status": "success",
        }
