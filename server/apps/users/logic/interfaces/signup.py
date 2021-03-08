import abc
from dataclasses import dataclass

from apps.users.models import User


@dataclass(frozen=True)
class SignupData:
    """Data for create user."""

    login: str
    password: str
    email: str
    name: str


@dataclass(frozen=True)
class SocialSignupData:
    """Data for create user."""

    email: str
    login: str
    name: str
    avatar: str


class ISignupService(abc.ABC):
    """Signup user interface."""

    @abc.abstractmethod
    def signup(self, signup_data: SignupData) -> User:
        """Signup user by provided data."""

    @abc.abstractmethod
    def signup_from_social(self, signup_data: SocialSignupData) -> User:
        """Signup user by provided data from social services."""
