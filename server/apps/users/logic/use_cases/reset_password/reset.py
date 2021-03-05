from dataclasses import dataclass

import injector

from apps.core.logic.use_cases import BaseUseCase
from apps.users.logic.interfaces import ITokenService
from apps.users.logic.interfaces.reset_password_request import (
    IResetPasswordRequestService,
)
from apps.users.logic.use_cases.reset_password.errors import (
    CodeValidationError,
    EmailNotExistsError,
)
from apps.users.models import Token, User


@dataclass(frozen=True)
class InputDto:
    """Password reset input data."""

    email: str
    code: str
    password: str


@dataclass(frozen=True)
class OutputDto:
    """Login output dto."""

    token: Token


class UseCase(BaseUseCase):
    """Use case for reset password."""

    @injector.inject
    def __init__(
        self,
        token_service: ITokenService,
        reset_password_service: IResetPasswordRequestService,
    ):
        """Initializing."""
        self._token_service = token_service
        self._reset_password_service = reset_password_service

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        user = self._get_user(input_dto)

        self._check_code(user, input_dto)
        user.set_password(input_dto.password)
        user.save()

        return OutputDto(
            token=self._token_service.create_user_token(user),
        )

    def _get_user(self, input_dto) -> User:
        """Get user by params from input dto."""
        user = User.objects.filter(email=input_dto.email).first()

        if not user:
            raise EmailNotExistsError()

        return user

    def _check_code(self, user, input_dto) -> None:
        if not self._reset_password_service.code_valid(user, input_dto.code):
            raise CodeValidationError()
