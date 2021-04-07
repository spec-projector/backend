from tests.test_billing.factories import ChangeSubscriptionRequestFactory
from tests.test_users.factories.user import UserFactory


def test_none(user, ghl_client, ghl_raw):
    """Test empty."""
    ghl_client.set_user(user)

    response = ghl_client.execute(ghl_raw("me_subscription"))

    assert "errors" not in response
    dto = response["data"]["me"]["changeSubscriptionRequest"]
    assert dto is None


def test_single_active(user, ghl_client, ghl_raw):
    """Test single active."""
    request = ChangeSubscriptionRequestFactory.create(user=user)
    ghl_client.set_user(user)

    response = ghl_client.execute(ghl_raw("me_subscription"))

    assert "errors" not in response
    dto = response["data"]["me"]["changeSubscriptionRequest"]
    assert dto is not None
    assert int(dto["id"]) == request.id


def test_many(user, ghl_client, ghl_raw):
    """Test many."""
    request = ChangeSubscriptionRequestFactory.create(user=user)
    ChangeSubscriptionRequestFactory.create_batch(
        2,
        is_active=False,
        user=user,
    )
    ghl_client.set_user(user)

    response = ghl_client.execute(ghl_raw("me_subscription"))

    assert "errors" not in response
    dto = response["data"]["me"]["changeSubscriptionRequest"]
    assert dto is not None
    assert int(dto["id"]) == request.id


def test_another_user(user, ghl_client, ghl_raw):
    """Test another user."""
    another_user = UserFactory.create()
    ChangeSubscriptionRequestFactory.create(user=another_user)

    ghl_client.set_user(user)

    response = ghl_client.execute(ghl_raw("me_subscription"))

    assert "errors" not in response
    dto = response["data"]["me"]["changeSubscriptionRequest"]
    assert dto is None
