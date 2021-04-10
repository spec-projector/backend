from dataclasses import asdict, dataclass

import injector
from rest_framework import serializers

from apps.billing.logic.interfaces import ISubscriptionService
from apps.core.logic.use_cases import BaseUseCase
from apps.users.logic.interfaces import ISignupService, ITokenService
from apps.users.logic.interfaces.signup import SignupData
from apps.users.logic.use_cases.register.errors import (
    RegistrationInputError,
    UserAlreadyExistsError,
)
from apps.users.models import Token, User


class RegistrationInputSerializer(serializers.Serializer):
    """Registration serializer."""

    first_name = serializers.CharField(
        max_length=50,  # noqa: WPS432
        required=True,
    )
    last_name = serializers.CharField(
        max_length=50,  # noqa: WPS432
        required=True,
    )
    email = serializers.EmailField(
        max_length=50,  # noqa: WPS432
        required=True,
    )
    password = serializers.CharField(required=True)


@dataclass(frozen=True)
class InputDto:
    """Register input data."""

    first_name: str
    last_name: str
    email: str
    password: str


@dataclass(frozen=True)
class OutputDto:
    """Register output dto."""

    token: Token


class UseCase(BaseUseCase):
    """Use case for register new user."""

    @injector.inject
    def __init__(
        self,
        token_service: ITokenService,
        signup_service: ISignupService,
        subscription_service: ISubscriptionService,
    ):
        """Initializing."""
        self._token_service = token_service
        self._signup_service = signup_service
        self._subscription_service = subscription_service

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        self._validate_data(input_dto)

        user = self._signup_service.signup(
            SignupData(
                first_name=input_dto.first_name,
                password=input_dto.password,
                email=input_dto.email,
                last_name=input_dto.last_name,
            ),
        )

        self._subscription_service.add_default_subscription(user)

        return OutputDto(
            token=self._token_service.create_user_token(user),
        )

    def _validate_data(self, input_dto) -> None:
        """Validate input data."""
        serializer = RegistrationInputSerializer(data=asdict(input_dto))

        if not serializer.is_valid():
            raise RegistrationInputError()

        validated_data = serializer.validated_data

        if User.objects.filter(email=validated_data["email"]).exists():
            raise UserAlreadyExistsError()
