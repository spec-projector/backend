from dataclasses import dataclass

from apps.core.logic.use_cases import BaseUseCase
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
        input_dto.user.set_password(input_dto.password)
        input_dto.user.save()

        return OutputDto(ok=True)
