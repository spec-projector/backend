from .gitlab.login import LoginGitlabMutation
from .login import LoginMutation
from .logout import LogoutMutation


class AuthMutations:
    login_gitlab = LoginGitlabMutation.Field()
    login = LoginMutation.Field()
    logout = LogoutMutation.Field()
