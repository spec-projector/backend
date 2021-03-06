from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseCommandMutation
from apps.core.logic import commands
from apps.projects.graphql.types import ProjectAssetType
from apps.projects.logic.commands.project_asset import (
    create as project_asset_create,
)


class CreateProjectAssetInput(graphene.InputObjectType):
    """Input for create project asset."""

    project = graphene.ID(required=True)
    url = graphene.String(required=True)


class CreateProjectAssetMutation(BaseCommandMutation):
    """Create project asset mutation."""

    class Meta:
        auth_required = True

    class Arguments:
        input = graphene.Argument(  # noqa: WPS125
            CreateProjectAssetInput,
            required=True,
        )

    project_asset = graphene.Field(ProjectAssetType)

    @classmethod
    def build_command(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> commands.ICommand:
        """Build command."""
        return project_asset_create.Command(
            user=info.context.user,  # type: ignore
            data=project_asset_create.ProjectAssetDto(**kwargs.get("input")),
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        command_result: project_asset_create.CommandResult,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {
            "project_asset": command_result.project_asset,
        }
