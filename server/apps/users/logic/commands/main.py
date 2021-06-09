from apps.users.logic.commands import change_password, register, user
from apps.users.logic.commands.auth import (
    login,
    logout,
    social_complete_login,
    social_login,
)
from apps.users.logic.commands.me import update, upload_avatar
from apps.users.logic.commands.reset_password import reset, send_password_reset

COMMANDS = (
    (login.LoginCommand, login.CommandHandler),
    (logout.LogoutCommand, logout.CommandHandler),
    (social_login.SocialLoginCommand, social_login.CommandHandler),
    (
        social_complete_login.SocialCompleteLoginCommand,
        social_complete_login.CommandHandler,
    ),
    (change_password.ChangePasswordCommand, change_password.CommandHandler),
    (update.MeUpdateCommand, update.CommandHandler),
    (upload_avatar.MeUploadAvatarCommand, upload_avatar.CommandHandler),
    (register.RegisterCommand, register.CommandHandler),
    (reset.ResetPasswordCommand, reset.CommandHandler),
    (
        send_password_reset.SendPasswordResetCommand,
        send_password_reset.CommandHandler,
    ),
    (user.UpdateUserActivityCommand, user.CommandHandler),
)
