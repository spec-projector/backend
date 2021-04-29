from typing import Dict, Optional

import graphene
from graphql import ResolveInfo
from jnt_django_graphene_toolbox.fields import BitField

from apps.core.graphql.mutations.command import BaseCommandMutation
from apps.core.logic import commands
from apps.projects.graphql.mutations.project.inputs import BaseProjectInput
from apps.projects.graphql.types.project import ProjectType
from apps.projects.logic.commands.project import update as project_update


class ProjectMemberInput(graphene.InputObjectType):
    """Project member input type."""

    id = graphene.ID(required=True)  # noqa: WPS125
    roles = BitField(required=True)


class UpdateProjectInput(BaseProjectInput):
    """Input for update project."""

    users = graphene.Argument(graphene.List(ProjectMemberInput))


class UpdateProjectMutation(BaseCommandMutation):
    """Update project mutation."""

    class Meta:
        auth_required = True

    class Arguments:
        id = graphene.ID(required=True)  # noqa: WPS125
        input = graphene.Argument(UpdateProjectInput)  # noqa: WPS125

    project = graphene.Field(ProjectType)

    @classmethod
    def build_command(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> commands.ICommand:
        """Prepare use case input data."""
        return project_update.UpdateProjectCommand(
            user=info.context.user,  # type: ignore
            project=kwargs["id"],
            data=project_update.ProjectDto(**kwargs.get("input")),
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        command_result: project_update.UpdateProjectCommandResult,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {
            "project": command_result.project,
        }
