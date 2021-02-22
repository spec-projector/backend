import abc
from dataclasses import dataclass

import injector
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.logic.errors import BaseApplicationError
from apps.core.logic.use_cases import BaseUseCase
from apps.core.services.errors import BaseInfrastructureError
from apps.users.logic.interfaces import ILoginService, ITokenService
from apps.users.models import Token


@dataclass(frozen=True)
class InputDto:
    """Login input data."""

    username: str
    password: str


@dataclass(frozen=True)
class OutputDto:
    """Login output dto."""

    token: Token


class LoginError(BaseApplicationError, metaclass=abc.ABCMeta):
    """Generic login error."""


class EmptyCredentialsError(LoginError):
    """Empty credentials error."""

    code = "empty_credentials"
    message = _("MSG__MUST_INCLUDE_LOGIN_AND_PASSWORD")


class UseCase(BaseUseCase):
    """Use case for retrieve issue."""

    @injector.inject
    def __init__(
        self,
        login_service: ILoginService,
        token_service: ITokenService,
    ):
        """Initializing."""
        self._login_service = login_service
        self._token_service = token_service

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        self._validate_input(input_dto)

        try:

            user = self._login_service.login(
                input_dto.username,
                input_dto.password,
            )
        except BaseInfrastructureError as err:
            raise LoginError(err.code, str(err))
        else:
            user.last_login = timezone.now()
            user.save(update_fields=("last_login",))

            token = self._token_service.create_user_token(user)
            return OutputDto(
                token=token,
            )

    def _validate_input(self, input_dto: InputDto) -> None:
        if not input_dto.username or not input_dto.password:
            raise EmptyCredentialsError()
