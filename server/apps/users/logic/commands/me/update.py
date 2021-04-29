from dataclasses import asdict, dataclass

from apps.core.logic import commands
from apps.users.models import User


@dataclass(frozen=True)
class MeUpdateCommand(commands.ICommand):
    """Update me."""

    user: User
    first_name: str = ""
    last_name: str = ""


@dataclass(frozen=True)
class MeUpdateCommandResult:
    """Update me output dto."""

    user: User


class CommandHandler(
    commands.ICommandHandler[MeUpdateCommand, MeUpdateCommandResult],
):
    """Update user."""

    def execute(self, command: MeUpdateCommand) -> MeUpdateCommandResult:
        """Main logic here."""
        return MeUpdateCommandResult(user=self._update_user(command))

    def _update_user(self, command: MeUpdateCommand) -> User:
        """Update user fields from input dto."""
        user_data = asdict(command)
        user = user_data.pop("user")

        for field, field_value in user_data.items():
            if field_value:
                setattr(user, field, field_value)
        user.save()

        return user
