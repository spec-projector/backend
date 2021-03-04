from apps.users.graphql.mutations import auth, register
from apps.users.graphql.mutations import reset_password as reset_pwd


class UsersMutations:
    """A class represents list of available mutations."""

    social_login = auth.SocialLoginMutation.Field()
    social_login_complete = auth.SocialLoginCompleteMutation.Field()

    login = auth.LoginMutation.Field()
    logout = auth.LogoutMutation.Field()
    register = register.RegisterMutation.Field()
    reset_password = reset_pwd.ResetPasswordMutation.Field()
    send_password_reset_security_code = (
        reset_pwd.SendPasswordResetSecurityCodeMutation.Field()
    )
