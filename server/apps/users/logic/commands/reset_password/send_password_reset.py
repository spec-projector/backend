from dataclasses import dataclass

import injector
from django.utils.translation import gettext_lazy as _

from apps.core.logic import commands
from apps.core.logic.interfaces import IEmailService
from apps.users.logic.commands.reset_password.errors import EmailNotExistsError
from apps.users.logic.interfaces.reset_password_request import (
    IResetPasswordRequestService,
)
from apps.users.models import User

EMAIL_TEMPLATE = "email/password_reset.html"


@dataclass(frozen=True)
class Command(commands.ICommand):
    """Password reset input data."""

    email: str


class CommandHandler(commands.ICommandHandler[Command, None]):
    """Retrieve issue."""

    @injector.inject
    def __init__(
        self,
        reset_password_service: IResetPasswordRequestService,
        email_service: IEmailService,
    ):
        """Initializing."""
        self._reset_password_service = reset_password_service
        self._email_service = email_service

    def execute(self, command: Command) -> None:
        """Main logic here."""
        user = self._get_user(command)
        reset_request = (
            self._reset_password_service.create_reset_password_request(user)
        )

        self._email_service.send_email(
            to=command.email,
            subject=_("MSG__SUBJECT_PASSWORD_RESET_SECURITY_CODE"),
            template=EMAIL_TEMPLATE,
            context={"secret_code": reset_request.code},
        )

    def _get_user(self, command: Command) -> User:
        """Get user by params from input dto."""
        user = User.objects.filter(email=command.email).first()
        if not user:
            raise EmailNotExistsError()

        return user
