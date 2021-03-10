from dataclasses import dataclass

from django.core.files.storage import default_storage
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

    user: User


class UseCase(BaseUseCase):
    """Use case for update user."""

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        user = input_dto.user
        old_avatar = user.avatar.path if user.avatar else None

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

        user.avatar = cropped_image
        user.save()

        if old_avatar and default_storage.exists(old_avatar):
            default_storage.delete(old_avatar)

        return OutputDto(user=user)
