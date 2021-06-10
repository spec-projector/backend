from dataclasses import dataclass

from django.utils import timezone

from apps.core.logic import commands
from apps.users.models import User


@dataclass(frozen=True)
class Command(commands.ICommand):
    """Update user activity."""

    user_pk: int


class CommandHandler(commands.ICommandHandler[Command, None]):
    """Update user activity."""

    def execute(self, command: Command) -> None:
        """Main logic here."""
        User.objects.filter(pk=command.user_pk).update(
            last_activity=timezone.now(),
        )
