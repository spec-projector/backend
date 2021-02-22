from dataclasses import dataclass
from typing import Union

from rest_framework import serializers

from apps.core import injector
from apps.core.logic.use_cases import BaseUseCase
from apps.core.services.couchdb import ICouchDBService
from apps.core.utils.objects import Empty, empty
from apps.projects.models import (
    FigmaIntegration,
    GitHubIntegration,
    GitLabIntegration,
    Project,
)
from apps.projects.use_cases.project.dto import (
    FigmaIntegrationDto,
    FigmaIntegrationDtoValidator,
    GitHubIntegrationDto,
    GitHubIntegrationDtoValidator,
    GitLabIntegrationDto,
    GitLabIntegrationDtoValidator,
)
from apps.users.models import User


class ProjectDtoValidator(serializers.Serializer):
    """Create project input."""

    title = serializers.CharField()
    is_public = serializers.BooleanField(default=False)
    description = serializers.CharField(default="", allow_blank=True)
    figma_integration = FigmaIntegrationDtoValidator(
        allow_null=True,
        required=False,
    )

    github_integration = GitHubIntegrationDtoValidator(
        allow_null=True,
        required=False,
    )

    gitlab_integration = GitLabIntegrationDtoValidator(
        allow_null=True,
        required=False,
    )


@dataclass(frozen=True)
class ProjectDto:
    """Create project data."""

    title: Union[str, Empty] = empty
    description: str = ""
    is_public: bool = False
    figma_integration: Union[str, FigmaIntegrationDto] = empty
    github_integration: Union[str, GitHubIntegrationDto] = empty
    gitlab_integration: Union[str, GitLabIntegrationDto] = empty


@dataclass(frozen=True)
class InputDto:
    """Create project input dto."""

    data: ProjectDto  # noqa: WPS110
    user: User


@dataclass(frozen=True)
class OutputDto:
    """Create project output dto."""

    project: Project


class UseCase(BaseUseCase):
    """Use case for creating projects."""

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        validated_data = self.validate_input(
            input_dto.data,
            ProjectDtoValidator,
        )

        project = Project.objects.create(
            title=validated_data["title"],
            is_public=validated_data["is_public"],
            description=validated_data["description"],
            owner=input_dto.user,
        )

        self._add_figma_integration(project, validated_data)
        self._add_github_integration(project, validated_data)
        self._add_gitlab_integration(project, validated_data)

        couch_db = injector.get(ICouchDBService)
        couch_db.create_database(project.db_name)
        couch_db.close()

        return OutputDto(project=project)

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
