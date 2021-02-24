from dataclasses import dataclass

import injector
from django.http import HttpRequest

from apps.core.logic.use_cases import BaseUseCase
from apps.users.logic.interfaces import ISocialLoginService
from apps.users.models import Token


@dataclass(frozen=True)
class InputDto:
    """GitLab login input data."""

    request: HttpRequest
    code: str
    state: str


@dataclass(frozen=True)
class OutputDto:
    """GitLab complete auth output dto."""

    token: Token


class UseCase(BaseUseCase):
    """Use case for retrieve issue."""

    @injector.inject
    def __init__(self, social_login_service: ISocialLoginService):
        """Initializing."""
        self._social_login_service = social_login_service

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        token = self._social_login_service.complete_login(
            input_dto.request,
            {
                "code": input_dto.code,
                "state": input_dto.state,
            },
        )

        return OutputDto(
            token=token,
        )
