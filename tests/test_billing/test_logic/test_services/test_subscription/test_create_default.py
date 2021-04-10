from apps.billing.models import Subscription
from apps.billing.models.enums import SubscriptionStatus
from tests.test_billing.factories import TariffFactory


def test_add(user, subscription_service):
    """Test add."""
    tariff = TariffFactory.create(is_default=True)

    subscription_service.add_default_subscription(user)

    subscription = Subscription.objects.filter(
        user=user,
        tariff=tariff,
    ).first()
    assert subscription is not None
    assert subscription.active_until is None
    assert subscription.status == SubscriptionStatus.ACTIVE


def test_no_default(user, subscription_service):
    """Test no default."""
    TariffFactory.create()

    subscription_service.add_default_subscription(user)

    assert not Subscription.objects.filter(user=user).exists()


def test_inactive_default(user, subscription_service):
    """Test inactive default."""
    TariffFactory.create(is_default=True, is_active=False)

    subscription_service.add_default_subscription(user)

    assert not Subscription.objects.filter(user=user).exists()


def test_no_tariffs(user, subscription_service):
    """Test no any tariffs."""
    subscription_service.add_default_subscription(user)

    assert not Subscription.objects.filter(user=user).exists()
