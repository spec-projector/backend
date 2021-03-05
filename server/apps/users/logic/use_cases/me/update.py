from dataclasses import asdict, dataclass
from typing import Dict

import injector
from django.db import models
from rest_framework import serializers

from apps.core.logic.use_cases import BaseUseCase
from apps.users.logic.interfaces import ITokenService
from apps.users.logic.use_cases.register.errors import (
    RegistrationInputError,
    UserAlreadyExistsError,
)
from apps.users.models import Token, User


class RegistrationInputSerializer(serializers.Serializer):
    """Registration serializer."""

    name = serializers.CharField(max_length=50, required=True)  # noqa: WPS432
    login = serializers.CharField(max_length=20, required=True)  # noqa: WPS432
    email = serializers.EmailField(
        max_length=50,  # noqa: WPS432
        required=True,
    )
    password = serializers.CharField(required=True)


@dataclass(frozen=True)
class InputDto:
    """Update input data."""

    user: User
    name: str
    avatar: str


@dataclass(frozen=True)
class OutputDto:
    """Register output dto."""

    user: User


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
        user = self._update_user(input_dto)

        return OutputDto(user=user)

    def _update_user(self, input_dto: InputDto) -> User:
        """Update user fields from input dto."""
        user_data = asdict(input_dto)
        user = user_data.pop("user")

        for field, field_value in user_data.items():
            if field_value:
                setattr(user, field, field_value)
        user.save()

        return user
