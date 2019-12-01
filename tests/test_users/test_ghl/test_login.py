from pytest import raises
from rest_framework.exceptions import AuthenticationFailed

from apps.users.graphql.mutations.login import LoginMutation
from apps.users.models import Token
from tests.conftest import DEFAULT_USERNAME, DEFAULT_USER_PASSWORD

GHL_QUERY_LOGIN = '''
mutation {{
    login(login: "{login}", password: "{password}") {{
        token {{
          key
        }}
    }}
}}
'''


def test_query(user, ghl_rf):
    assert not Token.objects.filter(user=user).exists()

    executed = ghl_rf.execute(GHL_QUERY_LOGIN.format(
        login=DEFAULT_USERNAME,
        password=DEFAULT_USER_PASSWORD,
    ))

    assert 'errors' not in executed

    token = Token.objects.filter(user=user).first()
    assert token is not None
    assert executed['data']['login']['token']['key'] == token.key


def test_mutation_success(user):
    assert not Token.objects.filter(user=user).exists()

    token = LoginMutation().do_mutate(
        None,
        None,
        DEFAULT_USERNAME,
        DEFAULT_USER_PASSWORD,
    )

    assert token is not None
    assert Token.objects.filter(user=user).exists()


def test_mutation_fail(user):
    assert not Token.objects.filter(user=user).exists()

    with raises(AuthenticationFailed):
        LoginMutation().do_mutate(
            None,
            None,
            'wrong{0}'.format(DEFAULT_USERNAME),
            DEFAULT_USER_PASSWORD,
        )

    assert not Token.objects.filter(user=user).exists()
