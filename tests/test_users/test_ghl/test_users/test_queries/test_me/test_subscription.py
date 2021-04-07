from tests.test_billing.factories import SubscriptionFactory


def test_none(user, ghl_client, ghl_raw):
    """Test empty subscription."""
    ghl_client.set_user(user)

    response = ghl_client.execute(ghl_raw("me_subscription"))

    assert "errors" not in response
    subscription_dto = response["data"]["me"]["subscription"]
    assert subscription_dto is None


def test_single_active(user, ghl_client, ghl_raw):
    """Test single active subscription."""
    subscription = SubscriptionFactory.create(user=user)
    ghl_client.set_user(user)

    response = ghl_client.execute(ghl_raw("me_subscription"))

    assert "errors" not in response
    subscription_dto = response["data"]["me"]["subscription"]
    assert subscription_dto is not None
    assert int(subscription_dto["id"]) == subscription.id
