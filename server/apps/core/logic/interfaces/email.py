import abc
from typing import Dict

from apps.core.models import EmailMessage


class IEmailService(abc.ABC):
    """Interface email service."""

    @abc.abstractmethod
    def send_email(
        self,
        to: str,
        subject: str,
        template: str,
        context,
    ) -> EmailMessage:
        """Create email."""
