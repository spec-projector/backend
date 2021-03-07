import abc
from dataclasses import dataclass

from apps.users.models import User


@dataclass(frozen=True)
class SignupUserData:
    """Data for create user."""

    email: str
    login: str
    name: str
    avatar: str


class ISignupService(abc.ABC):
    """Signup user interface."""

    @abc.abstractmethod
    def signup_user(self, signup_data: SignupUserData) -> User:
        """Signup user by provided data."""
