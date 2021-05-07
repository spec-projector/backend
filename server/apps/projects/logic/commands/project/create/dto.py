from dataclasses import dataclass
from typing import Union

from rest_framework import serializers

from apps.core.utils.objects import Empty, empty
from apps.media.models import Image
from apps.projects.logic.commands.project.dto import (
    FigmaIntegrationDto,
    FigmaIntegrationDtoValidator,
    GitHubIntegrationDto,
    GitHubIntegrationDtoValidator,
    GitLabIntegrationDto,
    GitLabIntegrationDtoValidator,
)


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
    emblem = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects,
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
    emblem: int = empty
