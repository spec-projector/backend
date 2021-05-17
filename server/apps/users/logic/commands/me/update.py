from dataclasses import asdict, dataclass
from typing import Optional

from rest_framework import serializers

from apps.core.logic import commands
from apps.media.models import Image
from apps.users.models import User


class MeUpdateDtoValidator(serializers.Serializer):
    """Update me input validator."""

    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    avatar = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects,
        required=False,
        allow_null=True,
    )


@dataclass(frozen=True)
class MeUpdateCommand(commands.ICommand):
    """Update me."""

    user: User
    avatar: Optional[int] = None
    first_name: str = ""
    last_name: str = ""


@dataclass(frozen=True)
class MeUpdateCommandResult:
    """Update me output dto."""

    user: User


class CommandHandler(
    commands.ICommandHandler[MeUpdateCommand, MeUpdateCommandResult],
):
    """Update user."""

    def execute(self, command: MeUpdateCommand) -> MeUpdateCommandResult:
        """Main logic here."""
        return MeUpdateCommandResult(user=self._update_user(command))

    def _update_user(self, command: MeUpdateCommand) -> User:
        """Update user fields from input dto."""
        user_data = asdict(command)
        user = user_data.pop("user")

        validator = MeUpdateDtoValidator(data=user_data)
        validator.is_valid(raise_exception=True)

        for field, field_value in validator.validated_data.items():
            if field_value:
                setattr(user, field, field_value)
        user.save()

        return user
