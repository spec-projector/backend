import abc
from dataclasses import asdict, dataclass

import injector
from django.utils.translation import gettext_lazy as _

from apps.core.logic.errors import BaseApplicationError
from apps.core.logic.use_cases import BaseUseCase
from apps.users.logic.interfaces import ITokenService
from apps.users.models import Token
from apps.users.services import RegistrationService


@dataclass(frozen=True)
class InputDto:
    """Register input data."""

    name: str
    login: str
    email: str
    password: str


@dataclass(frozen=True)
class OutputDto:
    """Register output dto."""

    token: Token


class RegisterError(BaseApplicationError, metaclass=abc.ABCMeta):
    """Generic login error."""


class EmptyCredentialsError(RegisterError):
    """Empty credentials error."""

    code = "empty_credentials"
    message = _("MSG__MUST_INCLUDE_LOGIN_AND_PASSWORD")


class UseCase(BaseUseCase):
    """Use case for register new user."""

    @injector.inject
    def __init__(
        self,
        token_service: ITokenService,
    ):
        """Initializing."""
        self._token_service = token_service

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        register_service = RegistrationService()
        user = register_service.register(**asdict(input_dto))

        return OutputDto(
            token=self._token_service.create_user_token(user),
        )
