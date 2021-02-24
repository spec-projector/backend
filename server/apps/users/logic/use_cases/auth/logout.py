from dataclasses import dataclass

import injector

from apps.core.logic.use_cases import BaseUseCase
from apps.users.logic.interfaces import ITokenService
from apps.users.models import Token


@dataclass(frozen=True)
class InputDto:
    """Logout unput data."""

    token: Token


class UseCase(BaseUseCase):
    """Logout service."""

    @injector.inject
    def __init__(self, token_service: ITokenService):
        """Initializing."""
        self._token_service = token_service

    def execute(self, input_dto: InputDto) -> None:
        """Main logic."""
        self._token_service.delete_token(input_dto.token)
