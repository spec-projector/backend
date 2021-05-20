from dataclasses import dataclass

import injector
from rest_framework import serializers

from apps.core.logic import commands
from apps.core.logic.errors import AccessDeniedApplicationError
from apps.core.logic.helpers.validation import validate_input
from apps.core.logic.interfaces import IExternalFilesService
from apps.media.models import File
from apps.projects.logic.interfaces import IFigmaServiceFactory
from apps.projects.logic.services.project_asset import (
    ProjectAssetPermissionsService,
)
from apps.projects.models import Project, ProjectAsset, ProjectAssetSource
from apps.users.models import User


class _ProjectAssetDtoValidator(serializers.Serializer):
    """Create project asset input."""

    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
    )
    url = serializers.CharField()


@dataclass(frozen=True)
class ProjectAssetDto:
    """Create project asset data."""

    project: str = ""
    url: str = ""


@dataclass(frozen=True)
class CreateProjectAssetCommand(commands.ICommand):
    """Create project asset input dto."""

    data: ProjectAssetDto  # noqa: WPS110
    user: User


@dataclass(frozen=True)
class CreateProjectAssetCommandResult:
    """Create project output."""

    project_asset: ProjectAsset


class CommandHandler(
    commands.ICommandHandler[
        CreateProjectAssetCommand,
        CreateProjectAssetCommandResult,
    ],
):
    """Create project asset."""

    @injector.inject
    def __init__(
        self,
        permissions_service: ProjectAssetPermissionsService,
        figma_service_factory: IFigmaServiceFactory,
        external_files_service: IExternalFilesService,
    ):
        """Initialize."""
        self._permissions_service = permissions_service
        self._figma_service_factory = figma_service_factory
        self._external_files_service = external_files_service

    def execute(
        self,
        command: CreateProjectAssetCommand,
    ) -> CreateProjectAssetCommandResult:
        """Main logic here."""
        validated_data = validate_input(
            command.data,
            _ProjectAssetDtoValidator,
        )

        can_upload = self._permissions_service.can_upload(
            command.user,
            validated_data["project"],
        )

        if not can_upload:
            raise AccessDeniedApplicationError()

        project_asset = ProjectAsset.objects.create(
            project=validated_data["project"],
            source=ProjectAssetSource.FIGMA,
        )

        project_asset.file = self._download_file(
            validated_data["url"],
            project_asset,
        )
        project_asset.save()

        return CreateProjectAssetCommandResult(
            project_asset=project_asset,
        )

    def _download_file(
        self,
        url: str,
        project_asset: ProjectAsset,
    ) -> File:
        """Download file."""
        figma_service = self._figma_service_factory.create(
            project_asset.project,
        )
        image_params = figma_service.get_image_params(url)
        image_url = figma_service.get_image_url(url)

        return self._external_files_service.download_file_from_url(
            image_url,
            image_params.title,
        )
