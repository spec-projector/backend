from constance import config
from django.template.loader import get_template

from apps.core.logic.interfaces import IEmailService
from apps.core.models import EmailMessage


class EmailService(IEmailService):
    """Interface email service."""

    def send_email(
        self,
        to: str,
        subject: str,
        template: str,
        context,
    ) -> EmailMessage:
        """Create email."""
        return EmailMessage.objects.create(
            to=to,
            subject=subject,
            html=get_template(template).render(context),
            sender=config.DEFAULT_FROM_EMAIL,
        )
