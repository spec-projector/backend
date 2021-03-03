from apps.core.services.email.email_sender import send_emails
from celery_app import app


@app.task
def send_emails_task():
    """Send emails."""
    send_emails()
