from apps.core.utils.objects import dict2obj
from apps.users.graphql.mutations.login import LoginMutation
from apps.users.models import Token
from tests.conftest import DEFAULT_USER_PASSWORD


def test_login(user, client):
    client.user = user
    info = dict2obj({'context': client})

    assert Token.objects.filter(user=user).exists() is False

    token = LoginMutation().do_mutate(
        None,
        info,
        user.login,
        DEFAULT_USER_PASSWORD,
    )

    assert token is not None
    assert Token.objects.filter(user=user).exists() is True
