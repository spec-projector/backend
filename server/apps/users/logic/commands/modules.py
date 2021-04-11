import injector

from apps.core.logic.commands.handlers import CommandHandler
from apps.users.logic.commands.auth import login


class UserCommandsModule(injector.Module):
    """Setup di for user application services."""

    def configure(self, binder: injector.Binder) -> None:
        """Bind services."""
        binder.bind(CommandHandler[login.Command], login.CommandHandler)
