import abc

from django.http import HttpRequest

from apps.users.models import Token


class ISocialLoginService(abc.ABC):
    """Social login service."""

    @abc.abstractmethod
    def begin_login(self, request: HttpRequest) -> str:
        """Initial login stage."""

    @abc.abstractmethod
    def complete_login(self, request, backend_data) -> Token:
        """Final login stage."""
