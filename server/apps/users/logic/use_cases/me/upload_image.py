from dataclasses import dataclass

from django.core.files.uploadedfile import InMemoryUploadedFile

from apps.core.logic.use_cases import BaseUseCase
from apps.core.services.image.cropper import CroppingParameters, crop_image
from apps.users.models import User


@dataclass(frozen=True)
class InputDto:
    """Upload image input data."""

    user: User
    file: InMemoryUploadedFile  # noqa: WPS110
    left: int
    top: int
    width: int
    height: int
    scale: float


@dataclass(frozen=True)
class OutputDto:
    """Upload image output dto."""

    path: str


class UseCase(BaseUseCase):
    """Use case for update user."""

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        cropped_image = crop_image(
            file_object=input_dto.file,
            parameters=CroppingParameters(
                left=input_dto.left,
                top=input_dto.top,
                width=input_dto.width,
                height=input_dto.height,
                scale=input_dto.scale,
            ),
        )

        input_dto.user.avatar = cropped_image
        input_dto.user.save()

        return OutputDto(path=input_dto.user.avatar.url)
