from dataclasses import dataclass

from django.core.files.uploadedfile import InMemoryUploadedFile

from apps.core.logic import commands
from apps.core.services.image.cropper import CroppingParameters, crop_image
from apps.users.models import User


@dataclass(frozen=True)
class Command(commands.ICommand):
    """Upload image command."""

    user: User
    file: InMemoryUploadedFile  # noqa: WPS110
    left: int
    top: int
    width: int
    height: int
    scale: float


@dataclass(frozen=True)
class CommandResult:
    """Upload image output dto."""

    user: User


class CommandHandler(commands.ICommandHandler[Command, CommandResult]):
    """Update user avatar."""

    def execute(self, command: Command) -> CommandResult:
        """Main logic here."""
        user = command.user

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

        return CommandResult(user=user)
