from abc import ABC, abstractmethod
from api.src.domus_ledger_api.modules.ledger.household.domain.entities.household import (
    Household,
)
from api.src.domus_ledger_api.shared_kernel.domain.result import Result


class AbstractHouseholdRepository(ABC):

    @abstractmethod
    async def get_household(self) -> Result[Household]:
        pass

    @abstractmethod
    async def create_household(self, household: Household) -> Result[None]:
        pass
