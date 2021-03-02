import abc

from apps.users.models import User


class IRegistrationService(abc.ABC):
    """Interface user registration service."""

    @abc.abstractmethod
    def register(
        self,
        name: str,
        email: str,
        login: str,
        password: str,
    ) -> User:
        """Register user by provided credentials."""
