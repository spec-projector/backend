import abc
from dataclasses import dataclass

from apps.users.models import User


@dataclass(frozen=True)
class CreateUserData:
    """Data for create user."""

    email: str
    login: str
    name: str
    avatar: str


class ICreateUserService(abc.ABC):
    """Interface create user."""

    @abc.abstractmethod
    def create_user(self, user_data: CreateUserData) -> User:
        """Create new user by provided data."""
