from apps.core.admin.inlines import BaseTabularInline
from apps.users.models import UserAccessToken


class UserAccessTokenInline(BaseTabularInline):
    """User access token inline."""

    model = UserAccessToken
    readonly_fields = ("key", "created_at")
    fields = ("name", "key", "created_at")
