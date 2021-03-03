import abc

from apps.core.models import EmailMessage


class IEmailService(abc.ABC):
    """Interface email service."""

    @abc.abstractmethod
    def send_email(self, to, subject, template, context) -> EmailMessage:
        """Create email."""
