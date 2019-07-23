from .login import LoginMutation
from .logout import LogoutMutation


class AuthMutations:
    login = LoginMutation.Field()
    logout = LogoutMutation.Field()
