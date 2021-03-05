from dataclasses import dataclass

from apps.core.logic.use_cases import BaseUseCase
from apps.users.logic.use_cases.change_password.errors import (
    PasswordNotSetError,
)
from apps.users.models import User


@dataclass(frozen=True)
class InputDto:
    """Change password input data."""

    password: str
    user: User


@dataclass(frozen=True)
class OutputDto:
    """Change password output dto."""

    ok: bool


class UseCase(BaseUseCase):
    """Use case for change password."""

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        password = self._validate_password(input_dto.password)

        input_dto.user.set_password(password)
        input_dto.user.save()

        return OutputDto(ok=True)

    def _validate_password(self, password: str) -> str:
        """Validate password."""
        if not password:
            raise PasswordNotSetError()

        return password
