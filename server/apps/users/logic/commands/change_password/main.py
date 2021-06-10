from dataclasses import dataclass

from apps.core.logic import commands
from apps.users.logic.commands.change_password.errors import (
    PasswordNotSetError,
)
from apps.users.models import User


@dataclass(frozen=True)
class Command(commands.ICommand):
    """Change password command."""

    password: str
    user: User


class CommandHandler(commands.ICommandHandler[Command, None]):
    """Change password."""

    def execute(self, command: Command) -> None:
        """Main logic here."""
        password = self._validate_password(command.password)

        command.user.set_password(password)
        command.user.save()

    def _validate_password(self, password: str) -> str:
        """Validate password."""
        if not password:
            raise PasswordNotSetError()

        return password
