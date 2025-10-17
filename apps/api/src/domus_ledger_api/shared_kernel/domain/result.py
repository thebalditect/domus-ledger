from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar, List, Union

from domus_ledger_api.shared_kernel.domain.error import Error

T = TypeVar("T")


@dataclass(frozen=True)
class Result(Generic[T]):
    _value: Optional[T]
    _errors: Optional[List[Error]]

    @property
    def is_success(self) -> bool:
        return self._errors is None or len(self._errors) == 0

    @property
    def is_failure(self) -> bool:
        return not self.is_success

    @property
    def value(self) -> T:
        if self.is_failure:
            raise AttributeError("Cannot access `value` on a failed result.")
        return self._value  # type:ignore[return-value]

    @property
    def errors(self) -> List[Error]:
        if self.is_success:
            raise AttributeError("Cannot access `errors` on a success result.")
        return self._errors or []

    @staticmethod
    def success(value: T) -> Result[T]:
        return Result(_value=value, _errors=[])

    @staticmethod
    def failure(errors: Union[Error, List[Error]]) -> Result[T]:

        if isinstance(errors, Error):
            errors = [errors]
        return Result(_value=None, _errors=errors)
