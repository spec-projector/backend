import abc
from typing import Type

from apps.core import injector
from apps.core.logic.commands import ICommand, ICommandHandler
from apps.core.logic.commands.handler import TResult


class ICommandBus(abc.ABC):
    """Commands dispatcher."""

    @abc.abstractmethod
    def register_handler(
        self,
        command_type: Type[ICommand],
        command_handler: Type[ICommandHandler[ICommand, TResult]],
    ) -> None:
        """Register command handler."""

    @abc.abstractmethod
    def dispatch(self, command: ICommand) -> TResult:
        """Send command and get result."""


class CommandBus(ICommandBus):
    """Queries dispatcher."""

    def __init__(self):
        """Initializing."""
        self._registry = {}

    def register_handler(
        self,
        command_type: Type[ICommand],
        command_handler: Type[ICommandHandler[ICommand, TResult]],
    ) -> None:
        """Register command handler."""
        self._registry[command_type] = command_handler

    def dispatch(self, command: ICommand) -> TResult:
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
