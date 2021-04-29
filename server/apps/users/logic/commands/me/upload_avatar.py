from dataclasses import dataclass

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile

from apps.core.logic import commands
from apps.core.services.image.cropper import CroppingParameters, crop_image
from apps.users.models import User


@dataclass(frozen=True)
class MeUploadAvatarCommand(commands.ICommand):
    """Upload image command."""

    user: User
    file: InMemoryUploadedFile  # noqa: WPS110
    left: int
    top: int
    width: int
    height: int
    scale: float


@dataclass(frozen=True)
class MeUploadAvatarCommandResult:
    """Upload image output dto."""

    user: User


class CommandHandler(
    commands.ICommandHandler[
        MeUploadAvatarCommand,
        MeUploadAvatarCommandResult,
    ],
):
    """Update user avatar."""

    def execute(
        self,
        command: MeUploadAvatarCommand,
    ) -> MeUploadAvatarCommandResult:
        """Main logic here."""
        user = command.user
        old_avatar = user.avatar.name

        cropped_image = crop_image(
            file_object=command.file,
            parameters=CroppingParameters(
                left=command.left,
                top=command.top,
                width=command.width,
                height=command.height,
                scale=command.scale,
            ),
        )

        user.avatar = cropped_image
        user.save()

        if old_avatar and default_storage.exists(old_avatar):
            default_storage.delete(old_avatar)

        return MeUploadAvatarCommandResult(user=user)
