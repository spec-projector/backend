import abc
from typing import Any, Type, TypeVar

from apps.core import injector
from apps.core.logic.commands import ICommandHandler

TCommand = TypeVar("TCommand")
TResult = TypeVar("TResult")


class ICommandBus(abc.ABC):
    """Commands dispatcher."""

    @abc.abstractmethod
    def register_handler(
        self,
        command_type: Type[TCommand],
        command_handler: Type[ICommandHandler[TCommand, TResult]],
    ) -> None:
        """Register command handler."""

    @abc.abstractmethod
    def dispatch(self, command: Any) -> Any:  # type: ignore
        """Send command and get result."""


class CommandBus(ICommandBus):
    """Commands dispatcher."""

    def __init__(self):
        """Initializing."""
        self._registry = {}

    def register_handler(
        self,
        command_type: Type[TCommand],
        command_handler: Type[ICommandHandler[TCommand, TResult]],
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
