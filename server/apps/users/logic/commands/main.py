from apps.core.logic.commands.bus import ICommandBus
from apps.users.logic.commands.auth import (
    login,
    logout,
    social_complete_login,
    social_login,
)


def register_commands(command_bus: ICommandBus):
    """Register commands handlers."""
    command_bus.register_handler(login.LoginCommand, login.CommandHandler)
    command_bus.register_handler(logout.LogoutCommand, logout.CommandHandler)
    command_bus.register_handler(
        social_login.SocialLoginCommand,
        social_login.CommandHandler,
    )
    command_bus.register_handler(
        social_complete_login.SocialCompleteLoginCommand,
        social_complete_login.CommandHandler,
    )
