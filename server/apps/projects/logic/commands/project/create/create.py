from dataclasses import dataclass

import injector

from apps.billing.logic.interfaces import ITariffLimitsService
from apps.core.logic import commands
from apps.core.logic.helpers.validation import validate_input
from apps.core.logic.interfaces import ICouchDBService
from apps.core.utils.bit_field import get_all_selected_bitfield
from apps.core.utils.objects import empty
from apps.projects.logic.commands.project.create import dto
from apps.projects.models import (
    FigmaIntegration,
    GitHubIntegration,
    GitLabIntegration,
    Project,
)
from apps.projects.models.enums import ProjectPermission
from apps.users.models import User


@dataclass(frozen=True)
class Command(commands.ICommand):
    """Create project input dto."""

    data: dto.ProjectDto  # noqa: WPS110
    user: User


@dataclass(frozen=True)
class CommandResult:
    """Create project output dto."""

    project: Project


class CommandHandler(commands.ICommandHandler[Command, CommandResult]):
    """Creating projects."""

    @injector.inject
    def __init__(
        self,
        tariff_limits_service: ITariffLimitsService,
        couch_db_service: ICouchDBService,
    ):
        """Initialize."""
        self._tariff_limits_service = tariff_limits_service
        self._couch_db_service = couch_db_service

    def execute(self, command: Command) -> CommandResult:
        """Main logic here."""
        validated_data = validate_input(
            command.data,
            dto.ProjectDtoValidator,
        )
        self._tariff_limits_service.assert_new_project_allowed(command.user)

        project = Project.objects.create(
            title=validated_data["title"],
            is_public=validated_data["is_public"],
            description=validated_data["description"],
            owner=command.user,
            emblem=validated_data.get("emblem"),
            public_role=validated_data.get("public_role"),
            public_permissions=get_all_selected_bitfield(ProjectPermission),
        )

        self._add_figma_integration(project, validated_data)
        self._add_github_integration(project, validated_data)
        self._add_gitlab_integration(project, validated_data)

        self._couch_db_service.create_database(project.db_name)

        return CommandResult(project=project)

    def _add_figma_integration(self, project: Project, validated_data) -> None:
        integration = validated_data.get("figma_integration")
        if integration and integration != empty:
            FigmaIntegration.objects.create(
                project=project,
                token=integration["token"],
            )

    def _add_github_integration(
        self,
        project: Project,
        validated_data,
    ) -> None:
        integration = validated_data.get("github_integration")
        if integration and integration != empty:
            GitHubIntegration.objects.create(
                project=project,
                token=integration["token"],
            )

    def _add_gitlab_integration(
        self,
        project: Project,
        validated_data,
    ) -> None:
        integration = validated_data.get("gitlab_integration")
        if integration and integration != empty:
            GitLabIntegration.objects.create(
                project=project,
                token=integration["token"],
            )
