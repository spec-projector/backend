from django.conf import settings
from jnt_django_graphene_toolbox.errors import GraphQLPermissionDenied

from tests.test_media.factories.image import ImageFactory

NEW_NAME = "new User NaMe"


def test_query(user, ghl_client, ghl_raw, image_in_memory):
    """Test raw query success."""
    user.avatar = ImageFactory.create(created_by=user)
    user.save()

    ghl_client.set_user(user)

    response = ghl_client.execute(
        ghl_raw("update_me"),
        variable_values={
            "input": {
                "firstName": NEW_NAME,
            },
        },
    )

    assert "errors" not in response

    user.refresh_from_db()
    me_response = response["data"]["updateMe"]["me"]

    assert me_response["id"] == str(user.id)
    assert me_response["firstName"] == user.first_name == NEW_NAME
    assert me_response["avatar"]["url"].startswith(
        "https://{0}".format(settings.DOMAIN_NAME),
    )


def test_success(user, ghl_auth_mock_info, update_me_mutation):
    """Test update me success."""
    update_me_mutation(
        root=None,
        info=ghl_auth_mock_info,
        input={
            "first_name": NEW_NAME,
        },
    )

    user.refresh_from_db()

    assert user.first_name == NEW_NAME


def test_not_auth(user, ghl_mock_info, update_me_mutation):
    """Test update me success."""
    response = update_me_mutation(
        root=None,
        info=ghl_mock_info,
        input={
            "first_name": NEW_NAME,
        },
    )

    assert isinstance(response, GraphQLPermissionDenied)
    assert user.first_name != NEW_NAME
