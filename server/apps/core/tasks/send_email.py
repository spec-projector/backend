from apps.core.services.email.dispatcher import EmailDispatcher
from celery_app import app
from apps.core import injector


@app.task
def send_emails_task():
    """Send emails."""
    dispatcher = injector.get(EmailDispatcher)
    dispatcher.send_emails()
