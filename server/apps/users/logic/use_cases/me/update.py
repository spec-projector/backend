from dataclasses import asdict, dataclass

from apps.core.logic.use_cases import BaseUseCase
from apps.users.models import User


@dataclass(frozen=True)
class InputDto:
    """Update input data."""

    user: User
    first_name: str = ""
    last_name: str = ""


@dataclass(frozen=True)
class OutputDto:
    """Update me output dto."""

    user: User


class UseCase(BaseUseCase):
    """Use case for update user."""

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        return OutputDto(user=self._update_user(input_dto))

    def _update_user(self, input_dto: InputDto) -> User:
        """Update user fields from input dto."""
        user_data = asdict(input_dto)
        user = user_data.pop("user")

        for field, field_value in user_data.items():
            if field_value:
                setattr(user, field, field_value)
        user.save()

        return user
