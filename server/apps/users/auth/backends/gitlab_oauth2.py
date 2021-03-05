from typing import Optional

from django.http import HttpResponseBadRequest
from django.utils import timezone
from social_core.backends.gitlab import GitLabOAuth2 as SocialGitLabOAuth2
from social_core.utils import handle_http_errors

from apps.core import injector
from apps.users.auth.backends.validate_backend import backend_is_valid
from apps.users.logic.interfaces import ITokenService, IUserService
from apps.users.logic.interfaces.create_user import CreateUserData
from apps.users.models import User


class GitLabOAuth2Backend(SocialGitLabOAuth2):
    """
    GitLab OAuth authentication backend.

    After successful authentication, a token is created.
    Create application: https://gitlab.com/profile/applications
    """

    @handle_http_errors
    def auth_complete(self, *args, **kwargs):
        """
        Do GitLab OAuth and return token.

        User must be exist in DB.
        """
        user = super().auth_complete(*args, **kwargs)

        if not user:
            return HttpResponseBadRequest("Invalid token")

        token_service = injector.get(ITokenService)
        token = token_service.create_user_token(user)

        user.last_login = timezone.now()
        user.save(update_fields=("last_login",))

        return token  # noqa: WPS331

    def get_redirect_uri(self, state=None):
        """Callback URL after approving access on Gitlab."""
        return self.setting("REDIRECT_URI")

    def authenticate(self, *args, **kwargs) -> Optional[User]:
        """Return authenticated user."""
        if not backend_is_valid(self.name, **kwargs):
            return None

        response = kwargs["response"]

        user = self._find_user(response["email"], response["username"])
        return user or self._create_user(response)

    def set_data(self, **kwargs):
        """Set data."""
        self.data = kwargs  # noqa: WPS110

    def _find_user(self, email: str, username: str) -> Optional[User]:
        """Find users by email or username."""
        user = User.objects.filter(email=email).first()
        if not user:
            user = User.objects.filter(login=username).first()

        return user

    def _create_user(self, response) -> User:
        """Create user from response data."""
        user_data = CreateUserData(
            email=response["email"],
            login=response["username"] or response["email"],
            name=response["name"],
            avatar=response["avatar_url"],
        )

        service = injector.get(IUserService)
        return service.create_user(user_data)
