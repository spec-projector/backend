from httpretty import httpretty
from social_core.backends.gitlab import GitLabOAuth2

from apps.billing.models import Subscription
from apps.billing.models.enums import SubscriptionStatus
from apps.users.logic.interfaces.social_login import SystemBackend
from apps.users.models import Token

KEY_TOKEN_TYPE = "token_type"  # noqa: S105
KEY_EXPIRES_IN = "expires_in"
KEY_ACCESS_TOKEN = "access_token"  # noqa: S105
KEY_REFRESH_TOKEN = "refresh_token"  # noqa: S105

ACCESS_TOKEN = "access_token"  # noqa: S105
REFRESH_TOKEN = "refresh_token"  # noqa: S105

CREATED_EMAIL = "vasiliy.popov@gitlab.com"


def test_complete_login(
    user,
    gl_mocker,
    social_login_complete_mutation,
    gl_token_request_info,
):
    """Test complete login."""
    gl_mocker.register_get(
        "/user",
        {
            "id": user.pk,
            "username": user.first_name,
            "name": user.last_name,
            "email": user.email,
        },
    )

    gl_mocker.base_api_url = GitLabOAuth2.ACCESS_TOKEN_URL
    gl_mocker.register_post(
        "",
        {
            KEY_ACCESS_TOKEN: ACCESS_TOKEN,
            KEY_REFRESH_TOKEN: REFRESH_TOKEN,
            KEY_TOKEN_TYPE: "bearer",
            KEY_EXPIRES_IN: 7200,
        },
    )

    response = social_login_complete_mutation(
        root=None,
        info=gl_token_request_info,
        code="test_code",
        state=gl_token_request_info.context.session["gitlab_state"],
        system=SystemBackend.GITLAB,
    )

    assert Token.objects.filter(pk=response.token.pk, user=user).exists()


def test_user_not_in_system(
    db,
    gl_mocker,
    social_login_complete_mutation,
    gl_token_request_info,
    assets,
):
    """Test complete login."""
    _register_mocks(gl_mocker, assets)

    response = social_login_complete_mutation(
        root=None,
        info=gl_token_request_info,
        code="test_code",
        state=gl_token_request_info.context.session["gitlab_state"],
        system=SystemBackend.GITLAB,
    )

    token = Token.objects.get(
        pk=response.token.pk,
        user__email=CREATED_EMAIL,
    )
    assert token.user.avatar


def test_subsciption_user_not_exists(  # noqa: WPS211
    db,
    default_tariff_config,
    default_tariff,
    gl_mocker,
    social_login_complete_mutation,
    gl_token_request_info,
    assets,
):
    """Test complete login. User will be created."""
    _register_mocks(gl_mocker, assets)

    response = social_login_complete_mutation(
        root=None,
        info=gl_token_request_info,
        code="test_code",
        state=gl_token_request_info.context.session["gitlab_state"],
        system=SystemBackend.GITLAB,
    )

    assert Subscription.objects.filter(
        user=response.token.user,
        status=SubscriptionStatus.ACTIVE,
        tariff=default_tariff,
    )


def _register_mocks(gl_mocker, assets) -> None:
    gl_mocker.register_get(
        "/user",
        assets.read_json("gitlab_user_response"),
    )
    httpretty.register_uri(
        httpretty.GET,
        "http://assets.gitlab-static.net/uploads/user/avatar/312/avatar.jpg",
        body=assets.open_file("avatar.jpg").read(),
    )

    gl_mocker.base_api_url = GitLabOAuth2.ACCESS_TOKEN_URL
    gl_mocker.register_post(
        "",
        {
            KEY_ACCESS_TOKEN: ACCESS_TOKEN,
            KEY_REFRESH_TOKEN: REFRESH_TOKEN,
            KEY_TOKEN_TYPE: "bearer",
            KEY_EXPIRES_IN: 7200,
        },
    )
