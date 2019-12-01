from apps.core.utils.objects import dict2obj
from apps.users.graphql.mutations.logout import LogoutMutation
from apps.users.models import Token
from apps.users.services.token import create_user_token


def test_logout(user, client):
    client.user = user
    client.auth = create_user_token(user)

    info = dict2obj({'context': client})

    assert Token.objects.filter(user=user).exists() is True

    LogoutMutation().mutate(None, info)

    assert Token.objects.filter(user=user).exists() is False
