from typing import Any, Type

from apps.core import injector
from apps.core.logic.interfaces import ICommandBus
from apps.core.logic.interfaces.command_bus import CommandHandler, TCommand


class CommandBus(ICommandBus):
    """Commands dispatcher."""

    def __init__(self):
        """Initializing."""
        self._registry = {}

    def register_handler(
        self,
        command_type: Type[TCommand],
        command_handler: Type[CommandHandler[TCommand]],
    ) -> None:
        """Register command handler."""
        self._registry[command_type] = command_handler

    def dispatch(self, command: Any) -> Any:  # type: ignore
        """Find command handler and executes it."""
        handler_type = self._registry.get(type(command))
        if not handler_type:
            raise ValueError(
                'Handler for command "{0}" is not registered'.format(
                    type(command),
                ),
            )
        command_handler = injector.get(handler_type)
        return command_handler.execute(command)
