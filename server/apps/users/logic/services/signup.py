from dataclasses import asdict

from apps.users.logic.interfaces import ISignupService
from apps.users.logic.interfaces.signup import SignupUserData
from apps.users.models import User


class SignupService(ISignupService):
    """Service for signup new user."""

    def signup_user(self, signup_data: SignupUserData) -> User:
        """Signup user by provided data."""
        return User.objects.create(is_staff=False, **asdict(signup_data))
