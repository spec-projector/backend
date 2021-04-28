import abc
from typing import Generic, TypeVar

TCommand = TypeVar("TCommand")
TResult = TypeVar("TResult")


class ICommandHandler(Generic[TCommand, TResult], metaclass=abc.ABCMeta):
    """Base command handler."""

    @abc.abstractmethod
    def execute(self, command: TCommand) -> TResult:
        """Main logic here."""
