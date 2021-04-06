from apps.core import injector
from apps.core.logic.interfaces import IEmailService
from apps.core.models.enums.email_status import EmailMessageStatus


def test_create_email(db):
    """Test create email."""
    email_service = injector.get(IEmailService)

    to = "to@mail.com"
    subject = "letter"

    email_message = email_service.send_email(
        to=to,
        subject=subject,
        template="email/password_reset.html",
        context={"secret_code": "test"},
    )

    assert email_message.to == to
    assert email_message.subject == subject
    assert email_message.status == EmailMessageStatus.READY
