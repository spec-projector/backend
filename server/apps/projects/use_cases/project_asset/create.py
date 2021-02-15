from dataclasses import dataclass
from tempfile import TemporaryFile

import requests
from django.core.files import File
from rest_framework import serializers

from apps.core import injector
from apps.core.application.use_cases import BaseUseCase
from apps.projects.models import Project, ProjectAsset
from apps.projects.models.project_asset import ProjectAssetSource
from apps.projects.services.projects.figma import (
    IFigmaService,
    IFigmaServiceFactory,
)
from apps.users.models import User

CHUNK_SIZE = 4096


class ProjectAssetDtoValidator(serializers.Serializer):
    """Create project asset input."""

    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        source="project",
    )
    url = serializers.CharField()


@dataclass(frozen=True)
class ProjectAssetDto:
    """Create project asset data."""

    project_id: str = ""
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

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        validated_data = self.validate_input(
            input_dto.data,
            ProjectAssetDtoValidator,
        )

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
        figma_client = self._get_figma_client(project_asset.project)
        image_params = figma_client.get_image_params(url)
        image_url = figma_client.get_image_url(url)

        self._save_to_field(
            project_asset.file,
            image_url,
            image_params.title,
        )

    def _save_to_field(self, field, image_url, title) -> None:
        with TemporaryFile() as temp_file:
            stream_request = requests.get(image_url, stream=True)
            for chunk in stream_request.iter_content(chunk_size=CHUNK_SIZE):
                temp_file.write(chunk)

            temp_file.seek(0)
            field.save("{0}.png".format(title), File(temp_file))

    def _get_figma_client(self, project: Project) -> IFigmaService:
        """Get figma client."""
        return injector.get(IFigmaServiceFactory).create(project)
