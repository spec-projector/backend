from dataclasses import dataclass
from tempfile import TemporaryFile

import injector
import requests
from django.core.files import File
from rest_framework import serializers

from apps.core.logic.errors import AccessDeniedApplicationError
from apps.core.logic.use_cases import BaseUseCase
from apps.projects.logic.interfaces.figma import IFigmaServiceFactory
from apps.projects.logic.services.project_asset import (
    ProjectAssetPermissionsService,
)
from apps.projects.models import Project, ProjectAsset, ProjectAssetSource
from apps.users.models import User

CHUNK_SIZE = 4096


class ProjectAssetDtoValidator(serializers.Serializer):
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
class InputDto:
    """Create project asset input dto."""

    data: ProjectAssetDto  # noqa: WPS110
    user: User


@dataclass(frozen=True)
class OutputDto:
    """Create project output dto."""

    project_asset: ProjectAsset


class UseCase(BaseUseCase):
    """Use case for creating project asset."""

    @injector.inject
    def __init__(
        self,
        permissions_service: ProjectAssetPermissionsService,
        figma_service_factory: IFigmaServiceFactory,
    ):
        """Initialize."""
        self._permissions_service = permissions_service
        self._figma_service_factory = figma_service_factory

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        validated_data = self.validate_input(
            input_dto.data,
            ProjectAssetDtoValidator,
        )

        can_upload = self._permissions_service.can_upload_project_asset(
            input_dto.user,
            validated_data["project"],
        )

        if not can_upload:
            raise AccessDeniedApplicationError()

        project_asset = ProjectAsset.objects.create(
            project=validated_data["project"],
            source=ProjectAssetSource.FIGMA,
        )

        self._download_to_file_field(validated_data["url"], project_asset)

        return OutputDto(project_asset=project_asset)

    def _download_to_file_field(
        self,
        url: str,
        project_asset: ProjectAsset,
    ) -> None:
        """Download file to field."""
        figma_service = self._figma_service_factory.create(
            project_asset.project,
        )
        image_params = figma_service.get_image_params(url)
        image_url = figma_service.get_image_url(url)

        self._save_to_field(
            project_asset.file,
            image_url,
            image_params.title,
        )

    def _save_to_field(self, field, image_url, title) -> None:
        with TemporaryFile() as tmp_file:
            stream_request = requests.get(image_url, stream=True)
            for chunk in stream_request.iter_content(chunk_size=CHUNK_SIZE):
                tmp_file.write(chunk)

            tmp_file.seek(0)
            field.save("{0}.png".format(title), File(tmp_file))
