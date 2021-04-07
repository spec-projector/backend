from tests.test_billing.factories import ChangeSubscriptionRequestFactory
from tests.test_users.factories.user import UserFactory


def test_none(user, subscription_service):
    """Test empty."""
    request = subscription_service.get_user_change_subscription_request(user)
    assert request is None


def test_single_active(user, subscription_service):
    """Test single active."""
    request = ChangeSubscriptionRequestFactory.create(user=user)

    user_request = subscription_service.get_user_change_subscription_request(
        user,
    )

    assert user_request is not None
    assert user_request.pk == request.pk


def test_many(user, subscription_service):
    """Test many."""
    request = ChangeSubscriptionRequestFactory.create(user=user)
    ChangeSubscriptionRequestFactory.create_batch(
        2,
        is_active=False,
        user=user,
    )
    user_request = subscription_service.get_user_change_subscription_request(
        user,
    )

    assert user_request is not None
    assert user_request.pk == request.pk


def test_another_user(user, subscription_service):
    """Test another user."""
    another_user = UserFactory.create()
    ChangeSubscriptionRequestFactory.create(user=another_user)

    user_request = subscription_service.get_user_change_subscription_request(
        user,
    )
    assert user_request is None
