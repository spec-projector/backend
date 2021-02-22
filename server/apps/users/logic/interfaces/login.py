import abc

from apps.users.models import User


class ILoginService(abc.ABC):
    """User login service."""

    @abc.abstractmethod
    def login(self, username: str, password: str) -> User:
        """Login user by provided credentials."""
