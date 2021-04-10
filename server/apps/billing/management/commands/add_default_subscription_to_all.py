from django.core.management import BaseCommand

from apps.billing.logic.interfaces import ISubscriptionService
from apps.core import injector
from apps.users.models import User


class Command(BaseCommand):
    """Command update couchdb scheme."""

    def handle(self, *args, **options):  # noqa: WPS110
        """Handler."""
        users = User.objects.all()
        service = injector.get(ISubscriptionService)
        for user in users:
            subscription = service.get_user_subscription(user)
            if not subscription:
                service.add_default_subscription(user)
