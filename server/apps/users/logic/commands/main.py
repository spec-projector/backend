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
    (login.Command, login.CommandHandler),
    (logout.Command, logout.CommandHandler),
    (social_login.Command, social_login.CommandHandler),
    (
        social_complete_login.Command,
        social_complete_login.CommandHandler,
    ),
    (change_password.Command, change_password.CommandHandler),
    (update.Command, update.CommandHandler),
    (upload_avatar.Command, upload_avatar.CommandHandler),
    (register.Command, register.CommandHandler),
    (reset.Command, reset.CommandHandler),
    (
        send_password_reset.Command,
        send_password_reset.CommandHandler,
    ),
    (user.Command, user.CommandHandler),
)
