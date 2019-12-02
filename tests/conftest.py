import pytest
from graphene_django.rest_framework.tests.test_mutation import mock_info
from graphql import ResolveInfo

from tests.helpers.ghl_client import GraphQLClient
from tests.helpers.request_factory import RequestFactory

DEFAULT_USERNAME = 'user'
DEFAULT_USER_PASSWORD = 'password'


def pytest_addoption(parser):
    parser.addoption(
        '--runslow',
        action='store_true',
        default=False,
        help='run slow tests',
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption('--runslow'):
        skip = pytest.mark.skip(
            reason='--runslow runs only marked as slow tests',
        )
        for item in items:
            if 'slow' not in item.keywords:
                item.add_marker(skip)
    else:
        skip = pytest.mark.skip(reason='need --runslow option to run')
        for item in items:
            if 'slow' in item.keywords:
                item.add_marker(skip)


@pytest.fixture(autouse=True)  # type: ignore
def media_root(settings, tmpdir_factory) -> None:
    '''Forces django to save media files into temp folder.'''
    settings.MEDIA_ROOT = tmpdir_factory.mktemp('media', numbered=True)


@pytest.fixture(autouse=True)
def password_hashers(settings):
    '''Forces django to use fast password hashers for tests.'''
    settings.PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]


@pytest.fixture()
def user(db, django_user_model, django_username_field):
    """A Django user.

    This uses an existing user with username 'user', or creates a new one with
    password 'password'.
    """
    UserModel = django_user_model
    username_field = django_username_field

    try:
        user = UserModel._default_manager.get(
            **{username_field: DEFAULT_USERNAME},
        )
    except UserModel.DoesNotExist:
        user = UserModel._default_manager.create_user(
            DEFAULT_USERNAME,
            DEFAULT_USER_PASSWORD,
        )
    return user


@pytest.fixture()  # type: ignore
def rf() -> RequestFactory:
    return RequestFactory()


@pytest.fixture()  # type: ignore
def ghl_client() -> GraphQLClient:
    return GraphQLClient()


@pytest.fixture()  # type: ignore
def ghl_auth_mock_info(user, rf) -> ResolveInfo:
    rf.set_user(user)
    request = rf.get('/graphql/')

    info = mock_info()
    info.context = request

    return info


@pytest.fixture()  # type: ignore
def ghl_mock_info(user, rf) -> ResolveInfo:
    request = rf.get('/graphql/')

    info = mock_info()
    info.context = request

    return info
