from dataclasses import asdict, dataclass

import injector

from apps.core.logic.use_cases import BaseUseCase
from apps.users.logic.interfaces import ITokenService
from apps.users.models import User


@dataclass(frozen=True)
class InputDto:
    """Update input data."""

    user: User
    name: str
    avatar: str


@dataclass(frozen=True)
class OutputDto:
    """Update me output dto."""

    me: User


class UseCase(BaseUseCase):
    """Use case for update user."""

    @injector.inject
    def __init__(
        self,
        token_service: ITokenService,
    ):
        """Initializing."""
        self._token_service = token_service

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        user = self._update_user(input_dto)

        return OutputDto(me=user)

    def _update_user(self, input_dto: InputDto) -> User:
        """Update user fields from input dto."""
        user_data = asdict(input_dto)
        user = user_data.pop("user")

        for field, field_value in user_data.items():
            if field_value:
                setattr(user, field, field_value)
        user.save()

        return user
