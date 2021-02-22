import abc
import dataclasses
from typing import Dict, Generic, TypeVar

from apps.core.logic.errors import InvalidInputApplicationError
from apps.core.utils.objects import empty

TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")


class BaseUseCase(Generic[TInput, TOutput], metaclass=abc.ABCMeta):
    """Base class for use cases."""

    @abc.abstractmethod
    def execute(self, input_dto: TInput) -> TOutput:
        """Main logic here."""

    def validate_input(self, input_data, validator_class) -> Dict[str, object]:
        """
        Validate input data.

        Raise exception if data is invalid.
        """
        to_validate = {
            data_key: data_value
            for data_key, data_value in dataclasses.asdict(input_data).items()
            if data_value != empty
        }

        validator = validator_class(data=to_validate)
        if not validator.is_valid():
            raise InvalidInputApplicationError(validator.errors)

        return validator.validated_data
