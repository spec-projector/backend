from typing import Generator

import pytest


@pytest.fixture(autouse=True)
def _django_settings(settings, tmpdir_factory) -> None:
    """Forces django test settings."""
    settings.MEDIA_ROOT = tmpdir_factory.mktemp("media", numbered=True)
    settings.PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ]
    settings.STATICFILES_STORAGE = (
        "django.contrib.staticfiles.storage.StaticFilesStorage"
    )
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


@pytest.fixture(autouse=True)
def _constance_config(override_config) -> Generator[None, None, None]:
    """Forces constance config."""
    with override_config(
        DEFAULT_FROM_EMAIL="admin@mail.com",
    ):
        yield
