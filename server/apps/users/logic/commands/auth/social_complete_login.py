from dataclasses import dataclass

import injector
from django.http import HttpRequest

from apps.core.logic import commands
from apps.users.logic.interfaces import ISocialLoginService
from apps.users.logic.interfaces.social_login import SystemBackend
from apps.users.models import Token


@dataclass(frozen=True)
class Command(commands.ICommand):
    """Social login command."""

    request: HttpRequest
    code: str
    state: str
    system: SystemBackend


@dataclass(frozen=True)
class CommandResult:
    """Social complete auth output dto."""

    token: Token


class CommandHandler(commands.ICommandHandler[Command, CommandResult]):
    """Complete social login."""

    @injector.inject
    def __init__(self, social_login_service: ISocialLoginService):
        """Initializing."""
        self._social_login_service = social_login_service

    def execute(self, command: Command) -> CommandResult:
        """Main logic here."""
        token = self._social_login_service.complete_login(
            command.request,
            command.code,
            command.state,
            command.system,
        )

        return CommandResult(
            token=token,
        )
