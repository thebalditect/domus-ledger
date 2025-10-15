from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.src.domus_ledger_api.modules.ledger.household.domain.repositories.abtract_household_repository import (
    AbstractHouseholdRepository,
)

from api.src.domus_ledger_api.modules.ledger.household.domain.entities.household import (
    Household,
)
from api.src.domus_ledger_api.modules.ledger.household.infrastructure.mappers.household_mapper import (
    HouseholdMapper,
)
from api.src.domus_ledger_api.modules.ledger.household.infrastructure.models.householdorm import (
    HouseholdORM,
)
from api.src.domus_ledger_api.modules.ledger.household.domain.entities.errors import (
    HouseholdErrors,
)
from api.src.domus_ledger_api.shared_kernel.domain.result import Result


class SqlAlchemyHouseholdRepository(AbstractHouseholdRepository):

    def __init__(self, async_session: AsyncSession) -> None:
        self.async_session = async_session

    async def get_household(self) -> Result[Household]:

        household_orms = (
            await self.async_session.execute(select(HouseholdORM))
        ).scalars()

        if len(household_orms.all()) > 1:
            return Result[Household].failure(HouseholdErrors.multiple_household_found())

        household_orm = household_orms.first()

        if household_orm is None:
            return Result[Household].failure(HouseholdErrors.household_not_found())

        household = HouseholdMapper.to_domain(household_orm)

        return Result[Household].success(household)
