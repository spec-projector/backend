import abc

from apps.users.models import Token, User


class IResetPasswordRequestService(abc.ABC):
    """Interface reset password request service."""

    @abc.abstractmethod
    def create_reset_password_request(self, user: User) -> Token:
        """Create reset password request for user."""

    @abc.abstractmethod
    def code_valid(self, user: User, code: str) -> bool:
        """Validate code."""
