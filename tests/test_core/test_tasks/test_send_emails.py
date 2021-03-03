import pytest
from django.core import mail

from apps.core.models.choices.email_status import EmailMessageStatus
from apps.core.tasks import send_emails_task
from tests.test_core.factories.email_message import EmailMessageFactory


@pytest.mark.parametrize(
    ("status", "sent_count"),
    [
        (EmailMessageStatus.CREATED, 1),
        (EmailMessageStatus.SENT, 0),
        (EmailMessageStatus.ERROR, 0),
    ],
)
def test_send_any_emails(db, status, sent_count):
    """Test send any emails."""
    EmailMessageFactory.create(status=status)
    send_emails_task()

    assert len(mail.outbox) == sent_count


def test_send_email(db):
    """Test send email."""
    email_message = EmailMessageFactory.create()
    send_emails_task()

    email_message.refresh_from_db()

    assert email_message.status == EmailMessageStatus.SENT
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [email_message.to]
