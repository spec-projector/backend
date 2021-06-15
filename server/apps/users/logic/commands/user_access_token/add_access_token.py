from dataclasses import dataclass

from apps.core.logic import commands
from apps.users.models import User, UserAccessToken


@dataclass(frozen=True)
class UserAccessTokenDto:
    """Create user access token data."""

    name: str


@dataclass(frozen=True)
class Command(commands.ICommand):
    """Add user access token input dto."""

    data: UserAccessTokenDto  # noqa: WPS110
    user: User


@dataclass(frozen=True)
class CommandResult:
    """User access token output dto."""

    access_token: UserAccessToken


class CommandHandler(commands.ICommandHandler[Command, CommandResult]):
    """Add user access token."""

    def execute(self, command: Command) -> CommandResult:
        """Main logic here."""
        return CommandResult(
            access_token=UserAccessToken.objects.create(
                user=command.user,
                name=command.data.name,
            ),
        )
