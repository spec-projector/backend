from apps.core.middleware import LastActivityMiddleware


def test_update_last_activity(user, auth_rf):
    """Test update last activity."""
    user.last_activity = None
    user.save()

    middleware = LastActivityMiddleware(_mock_get_response)
    middleware(auth_rf.get(""))

    user.refresh_from_db(fields=["last_activity"])

    assert user.last_activity


def _mock_get_response(request):
    """Mock get response."""
    return request
