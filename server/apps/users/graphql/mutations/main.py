from apps.users.graphql.mutations import auth, change_password, me, register
from apps.users.graphql.mutations import reset_password as reset_pwd
from apps.users.graphql.mutations import user_access_token


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
    change_password = change_password.ChangePasswordMutation.Field()

    update_me = me.UpdateMeMutation.Field()
    upload_me_avatar = me.UploadMeAvatarMutation.Field()

    add_access_token = user_access_token.AddUserAccessTokenMutation.Field()
    delete_access_token = (
        user_access_token.DeleteUserAccessTokenMutation.Field()
    )
