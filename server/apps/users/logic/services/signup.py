from dataclasses import asdict

from apps.users.logic.interfaces import ISignupService
from apps.users.logic.interfaces.signup import SignupData, SocialSignupData
from apps.users.models import User


class SignupService(ISignupService):
    """Service for signup new user."""

    def signup(self, signup_data: SignupData) -> User:
        """Signup user by provided data."""
        return User.objects.create_user(
            login=signup_data.login,
            password=signup_data.password,
            email=signup_data.email,
            name=signup_data.name,
            is_staff=False,
        )

    def signup_from_social(self, signup_data: SocialSignupData) -> User:
        """Signup user by provided data."""
        return User.objects.create(is_staff=False, **asdict(signup_data))
