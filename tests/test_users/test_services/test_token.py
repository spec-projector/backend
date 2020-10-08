from datetime import timedelta

from django.utils import timezone

from apps.users.models import Token
from apps.users.services.token import clear_tokens, create_user_token

TOKEN_EXPIRE = 5


def test_create_user_token(user):
    """Test create user token."""
    user_tokens = list(
        Token.objects.filter(user=user).values_list("key", flat=True),
    )
    token = create_user_token(user)

    assert token
    assert token.key not in user_tokens


def test_clear_tokens(user, settings):
    """Test clear user token."""
    settings.REST_FRAMEWORK_TOKEN_EXPIRE = TOKEN_EXPIRE

    token = create_user_token(user)
    Token.objects.filter(pk=token.pk).update(
        created=timezone.now() - timedelta(minutes=TOKEN_EXPIRE + 1),
    )

    clear_tokens()

    assert not Token.objects.filter(pk=token.pk).exists()


def test_clear_tokens_not_expire(user, settings):
    """Test create user token if not expire."""
    settings.REST_FRAMEWORK_TOKEN_EXPIRE = TOKEN_EXPIRE

    token = create_user_token(user)

    clear_tokens()

    assert Token.objects.filter(pk=token.pk).exists()


def test_clear_tokens_token_expire_is_none(user, settings):
    """Test clear tokens if expire is none."""
    settings.REST_FRAMEWORK_TOKEN_EXPIRE = None

    token = create_user_token(user)
    clear_tokens()

    assert Token.objects.filter(pk=token.pk).exists()
