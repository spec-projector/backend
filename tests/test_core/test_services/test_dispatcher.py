import pytest
from django.core import mail

from apps.core import injector
from apps.core.models.enums.email_status import EmailMessageStatus
from apps.core.services.email import EmailDispatcher
from tests.test_core.factories.email_message import EmailMessageFactory


@pytest.fixture()
def dispatcher():
    """Init email dispatcher."""
    return injector.get(EmailDispatcher)


@pytest.mark.parametrize(
    ("status", "sent_count"),
    [
        (EmailMessageStatus.CREATED, 0),
        (EmailMessageStatus.READY, 1),
        (EmailMessageStatus.SENDING, 0),
        (EmailMessageStatus.SENT, 0),
        (EmailMessageStatus.ERROR, 0),
    ],
)
def test_send_any_emails(db, status, dispatcher, sent_count):
    """Test send any emails."""
    EmailMessageFactory.create(status=status)
    dispatcher.send_emails()

    assert len(mail.outbox) == sent_count


def test_send_email(db, dispatcher):
    """Test send email."""
    email_message = EmailMessageFactory.create(status=EmailMessageStatus.READY)
    dispatcher.send_emails()

    email_message.refresh_from_db()

    assert email_message.status == EmailMessageStatus.SENT
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [email_message.to]
