from pytest import raises
from rest_framework.exceptions import PermissionDenied

from apps.users.graphql.mutations.logout import LogoutMutation
from apps.users.models import Token

GHL_QUERY_LOGOUT = '''
mutation {
    logout {
        ok
    }
}
'''


def test_query(user, ghl_client):
    """Test logout query."""
    ghl_client.set_user(user)

    assert Token.objects.filter(user=user).exists()

    result = ghl_client.execute(GHL_QUERY_LOGOUT)

    assert 'errors' not in result
    assert result['data']['logout']['ok']

    assert not Token.objects.filter(user=user).exists()


def test_success(user, ghl_auth_mock_info):
    """Test success logout."""

    assert Token.objects.filter(user=user).exists()

    LogoutMutation().mutate(None, ghl_auth_mock_info)

    assert not Token.objects.filter(user=user).exists()


def test_non_auth(user, ghl_mock_info):
    """Test logout if user is not logged."""
    with raises(PermissionDenied):
        LogoutMutation().mutate(None, ghl_mock_info)
