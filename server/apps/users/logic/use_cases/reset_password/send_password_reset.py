from dataclasses import dataclass

import injector

from apps.core.logic.use_cases import BaseUseCase
from apps.users.logic.interfaces.reset_password_request import (
    IResetPasswordRequestService,
)
from apps.users.logic.use_cases.reset_password.errors import (
    EmailNotExistsError,
)
from apps.users.models import User


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
    ):
        """Initializing."""
        self._reset_password_service = reset_password_service

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        user = self._get_user(input_dto)
        reset_request = (
            self._reset_password_service.create_reset_password_request(user)
        )
        # TODO: send_email with code from reset request: reset_request.code

        return OutputDto(ok=True)

    def _get_user(self, input_dto) -> User:
        """Get user by params from input dto."""
        user = User.objects.filter(email=input_dto.email).first()

        if not user:
            raise EmailNotExistsError()

        return user
