from jnt_django_toolbox.decorators import one_at_time

from apps.core import injector
from apps.core.services.email.dispatcher import EmailDispatcher
from celery_app import app


@app.task
@one_at_time
def send_emails_task():
    """Send emails."""
    dispatcher = injector.get(EmailDispatcher)
    dispatcher.send_emails()
