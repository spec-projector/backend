from dataclasses import dataclass

from django.utils import timezone

from apps.core.logic import commands
from apps.users.models import User


@dataclass(frozen=True)
class UpdateUserActivityCommand(commands.ICommand):
    """Update user activity."""

    user_pk: int


class CommandHandler(
    commands.ICommandHandler[UpdateUserActivityCommand, None],
):
    """Update user activity."""

    def execute(self, command: UpdateUserActivityCommand) -> None:
        """Main logic here."""
        User.objects.filter(pk=command.user_pk).update(
            last_activity=timezone.now(),
        )
