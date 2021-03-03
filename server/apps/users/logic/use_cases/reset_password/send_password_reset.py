from dataclasses import dataclass

import injector
from django.utils.translation import gettext_lazy as _

from apps.core.logic.interfaces import IEmailService
from apps.core.logic.use_cases import BaseUseCase
from apps.users.logic.interfaces.reset_password_request import (
    IResetPasswordRequestService,
)
from apps.users.logic.use_cases.reset_password.errors import (
    EmailNotExistsError,
)
from apps.users.models import User

EMAIL_TEMPLATE = "email/password_reset.html"


@dataclass(frozen=True)
class InputDto:
    """Password reset input data."""

    email: str


@dataclass(frozen=True)
class OutputDto:
    """Login output dto."""

    ok: bool


class UseCase(BaseUseCase):
    """Use case for retrieve issue."""

    @injector.inject
    def __init__(
        self,
        reset_password_service: IResetPasswordRequestService,
        email_service: IEmailService,
    ):
        """Initializing."""
        self._reset_password_service = reset_password_service
        self._email_service = email_service

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        user = self._get_user(input_dto)
        reset_request = (
            self._reset_password_service.create_reset_password_request(user)
        )

        self._email_service.send_email(
            to=input_dto.email,
            subject=_("MSG__SUBJECT_PASSWORD_RESET_SECURITY_CODE"),
            template=EMAIL_TEMPLATE,
            context={"secret_code": reset_request.code},
        )

        return OutputDto(ok=True)

    def _get_user(self, input_dto) -> User:
        """Get user by params from input dto."""
        user = User.objects.filter(email=input_dto.email).first()

        if not user:
            raise EmailNotExistsError()

        return user
