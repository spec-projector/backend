from dataclasses import dataclass

import injector

from apps.core.logic import commands
from apps.users.logic.commands.reset_password.errors import (
    CodeValidationError,
    EmailNotExistsError,
)
from apps.users.logic.interfaces import ITokenService
from apps.users.logic.interfaces.reset_password_request import (
    IResetPasswordRequestService,
)
from apps.users.models import Token, User


@dataclass(frozen=True)
class Command(commands.ICommand):
    """Password reset command."""

    email: str
    code: str
    password: str


@dataclass(frozen=True)
class CommandResult:
    """Login output dto."""

    token: Token


class CommandHandler(commands.ICommandHandler[Command, CommandResult]):
    """Reset password."""

    @injector.inject
    def __init__(
        self,
        token_service: ITokenService,
        reset_password_service: IResetPasswordRequestService,
    ):
        """Initializing."""
        self._token_service = token_service
        self._reset_password_service = reset_password_service

    def execute(self, command: Command) -> CommandResult:
        """Main logic here."""
        user = self._get_user(command)

        self._check_code(user, command)
        user.set_password(command.password)
        user.save()

        return CommandResult(
            token=self._token_service.create_user_token(user),
        )

    def _get_user(self, command) -> User:
        """Get user by params from input dto."""
        user = User.objects.filter(email=command.email).first()
        if not user:
            raise EmailNotExistsError()

        return user

    def _check_code(self, user, command) -> None:
        if not self._reset_password_service.code_valid(user, command.code):
            raise CodeValidationError()
