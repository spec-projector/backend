from dataclasses import dataclass

import injector
from django.http import HttpRequest

from apps.core.logic import commands
from apps.users.logic.interfaces import ISocialLoginService
from apps.users.logic.interfaces.social_login import SystemBackend


@dataclass(frozen=True)
class SocialLoginCommand(commands.ICommand):
    """Social login input data."""

    request: HttpRequest
    system: SystemBackend


@dataclass(frozen=True)
class SocialLoginCommandResult:
    """Login output dto."""

    redirect_url: str


class CommandHandler(
    commands.ICommandHandler[
        SocialLoginCommand,
        SocialLoginCommandResult,
    ],
):
    """Social login."""

    @injector.inject
    def __init__(self, social_login_service: ISocialLoginService):
        """Initializing."""
        self._social_login_service = social_login_service

    def execute(self, command: SocialLoginCommand) -> SocialLoginCommandResult:
        """Main logic here."""
        redirect_url = self._social_login_service.begin_login(
            command.request,
            command.system,
        )

        return SocialLoginCommandResult(
            redirect_url=redirect_url,
        )
