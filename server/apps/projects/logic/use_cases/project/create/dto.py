from dataclasses import dataclass
from typing import Union

from rest_framework import serializers

from apps.core.utils.objects import Empty, empty
from apps.projects.logic.use_cases.project.dto import (
    FigmaIntegrationDto,
    FigmaIntegrationDtoValidator,
    GitHubIntegrationDto,
    GitHubIntegrationDtoValidator,
    GitLabIntegrationDto,
    GitLabIntegrationDtoValidator,
)
from apps.projects.models import Project
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
