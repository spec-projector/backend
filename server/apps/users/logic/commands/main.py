from apps.core.logic.commands.bus import ICommandBus
from apps.users.logic.commands.auth import login


def register_commands(command_bus: ICommandBus):
    """Register commands."""
    command_bus.register_handler(login.Command, login.CommandHandler)
