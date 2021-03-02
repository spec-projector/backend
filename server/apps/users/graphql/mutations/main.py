from apps.users.graphql.mutations import auth
from apps.users.graphql.mutations import reset_password as reset_pwd


class UsersMutations:
    """A class represents list of available mutations."""

    complete_gitlab_auth = auth.CompleteGitlabAuthMutation.Field()
    login_gitlab = auth.LoginGitlabMutation.Field()
    login = auth.LoginMutation.Field()
    logout = auth.LogoutMutation.Field()
    reset_password = reset_pwd.ResetPasswordMutation.Field()
    send_password_reset_security_code = (
        reset_pwd.SendPasswordResetSecurityCodeMutation.Field()
    )
