from social_core.backends.gitlab import GitLabOAuth2 as SocialGitLabOAuth2

from apps.users.logic.interfaces.signup import SocialSignupData
from apps.users.models import User
from apps.users.services.auth_backends.mixin import OAuth2BackendMixin


class GitLabOAuth2Backend(OAuth2BackendMixin, SocialGitLabOAuth2):
    """
    GitLab OAuth authentication backend.

    After successful authentication, a token is created.
    Create application: https://gitlab.com/profile/applications
    """

    def find_user(self, response):
        """Find user for response."""
        return User.objects.filter(email=response["email"]).first()

    def get_signup_data(self, response) -> SocialSignupData:
        """Return data for signup user."""
        return SocialSignupData(
            email=response["email"],
            first_name=response["username"],
            last_name=response["name"],
            avatar=response["avatar_url"],
        )
