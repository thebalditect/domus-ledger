from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self

from domus_ledger_api.modules.ledger.household.domain.repositories.abtract_household_repository import (
    AbstractHouseholdRepository,
)


class AbstractHouseholdUnitOfWork(ABC):

    repository: AbstractHouseholdRepository

    @abstractmethod
    async def __aenter__(self) -> Self:
        pass

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass
