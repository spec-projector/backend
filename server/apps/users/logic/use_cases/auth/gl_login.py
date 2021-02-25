from dataclasses import dataclass

import injector
from django.http import HttpRequest

from apps.core.logic.use_cases import BaseUseCase
from apps.users.logic.interfaces import ISocialLoginService


@dataclass(frozen=True)
class InputDto:
    """GitLab login input data."""

    request: HttpRequest


@dataclass(frozen=True)
class OutputDto:
    """Login output dto."""

    redirect_url: str


class UseCase(BaseUseCase):
    """Use case for retrieve issue."""

    @injector.inject
    def __init__(self, social_login_service: ISocialLoginService):
        """Initializing."""
        self._social_login_service = social_login_service

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        redirect_url = self._social_login_service.begin_login(
            input_dto.request,
        )

        return OutputDto(
            redirect_url=redirect_url,
        )
