import pytest
from django.core.exceptions import ValidationError


def test_clean_user_not_valid_login(user):
    """Test clean not valid login."""
    user.login = "a"
    with pytest.raises(ValidationError):
        user.full_clean()
