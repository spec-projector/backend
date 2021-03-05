from apps.users.graphql.mutations import auth, change_password, register
from apps.users.graphql.mutations import reset_password as reset_pwd
from apps.users.graphql.mutations import me


class UsersMutations:
    """A class represents list of available mutations."""

    complete_gitlab_auth = auth.CompleteGitlabAuthMutation.Field()
    login_gitlab = auth.LoginGitlabMutation.Field()
    login = auth.LoginMutation.Field()
    logout = auth.LogoutMutation.Field()
    register = register.RegisterMutation.Field()
    reset_password = reset_pwd.ResetPasswordMutation.Field()
    send_password_reset_security_code = (
        reset_pwd.SendPasswordResetSecurityCodeMutation.Field()
    )
    change_password = change_password.ChangePasswordMutation.Field()

    update_me = me.UpdateMeMutation.Field()
