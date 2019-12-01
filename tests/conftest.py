import pytest

from apps.users.models import User
from .base import Client, create_user


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


@pytest.fixture(scope='module')  # type: ignore
def client() -> Client:
    return Client()


@pytest.fixture(autouse=True, scope='function')  # type: ignore
def media_root(settings, tmpdir_factory) -> None:
    """Forces django to save media files into temp folder."""
    settings.MEDIA_ROOT = tmpdir_factory.mktemp('media', numbered=True)


@pytest.fixture(autouse=True, scope='function')
def password_hashers(settings):
    """Forces django to use fast password hashers for tests."""
    settings.PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]


@pytest.fixture()  # type: ignore
def user(db) -> User:
    return create_user()
