from constance import config
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone

from apps.core.models import EmailMessage
from apps.core.models.choices.email_status import EmailMessageStatus


class EmailSender:
    """Email sender."""

    def send_emails(self) -> None:
        """Send emails."""
        for email_message in self._get_emails_for_send():
            self.send_email(email_message)

    def send_email(self, email_message: EmailMessage) -> None:
        """Send email."""
        try:
            send_mail(
                subject=email_message.subject,
                message=email_message.html,
                from_email=email_message.sender or config.DEFAULT_FROM_EMAIL,
                recipient_list=[email_message.to],
                html_message=email_message.html,
            )
        except Exception as error:  # TODO: catch any errors for logging.
            email_message.status = EmailMessageStatus.ERROR
            email_message.status_info = str(error)
        else:
            email_message.status = EmailMessageStatus.SENT
            email_message.sent_at = timezone.now()

        email_message.save()

    def _get_emails_for_send(self) -> models.QuerySet:
        """Get messages for send."""
        return EmailMessage.objects.filter(status=EmailMessageStatus.CREATED)


def send_emails() -> None:
    """Send emails."""
    EmailSender().send_emails()
