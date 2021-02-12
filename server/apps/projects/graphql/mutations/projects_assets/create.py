from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseUseCaseMutation
from apps.projects.graphql.types import ProjectAssetType
from apps.projects.use_cases.project_asset import (
    create as project_asset_create,
)


class CreateProjectAssetInput(graphene.InputObjectType):
    """Input for create project asset."""

    project_id = graphene.ID(required=True)
    url = graphene.String(required=True)


class CreateProjectAssetMutation(BaseUseCaseMutation):
    """Create project asset mutation."""

    class Meta:
        use_case_class = project_asset_create.UseCase
        auth_required = True

    class Arguments:
        input = graphene.Argument(  # noqa: WPS125
            CreateProjectAssetInput,
            required=True,
        )

    project_asset = graphene.Field(ProjectAssetType)

    @classmethod
    def get_input_dto(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ):
        """Prepare use case input data."""
        return project_asset_create.InputDto(
            user=info.context.user,  # type: ignore
            data=project_asset_create.ProjectAssetDto(**kwargs.get("input")),
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        output_dto: project_asset_create.OutputDto,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {
            "project_asset": output_dto.project_asset,
        }
