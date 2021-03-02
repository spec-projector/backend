from django.db import models
from rest_framework import serializers

from apps.users.models import User
from apps.users.services.register.errors import (
    RegistrationInputError,
    UserAlreadyExistsError,
)


class RegistrationSerializer(serializers.Serializer):
    """Registration serializer."""

    name = serializers.CharField(max_length=50, required=True)  # noqa: WPS432
    login = serializers.CharField(max_length=20, required=True)  # noqa: WPS432
    email = serializers.EmailField(
        max_length=50,  # noqa: WPS432
        required=True,
    )
    password = serializers.CharField(required=True)


class RegistrationService:
    """Registration service."""

    def register(
        self,
        name: str,
        email: str,
        login: str,
        password: str,
    ) -> User:
        """Register user."""
        self._validate_data(
            name=name,
            email=email,
            login=login,
            password=password,
        )

        return User.objects.create_user(
            login=login,
            password=password,
            email=email,
            name=name,
            is_staff=False,
        )

    def _validate_data(self, **kwargs) -> None:
        """Validate input data."""
        serializer = RegistrationSerializer(data=kwargs)

        if not serializer.is_valid():
            raise RegistrationInputError()

        validated_data = serializer.validated_data

        query = models.Q(login=validated_data["login"]) | models.Q(
            email=validated_data["email"],
        )

        if User.objects.filter(query).exists():
            raise UserAlreadyExistsError()
