import abc
from typing import Generic, TypeVar

TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")


class BaseUseCase(Generic[TInput, TOutput], metaclass=abc.ABCMeta):
    """Base class for use cases."""

    @abc.abstractmethod
    def execute(self, input_dto: TInput) -> TOutput:
        """Main logic here."""
