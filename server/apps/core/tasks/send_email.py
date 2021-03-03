from apps.core.services.email.dispatcher import EmailDispatcher
from celery_app import app


@app.task
def send_emails_task():
    """Send emails."""
    EmailDispatcher().send_emails()
