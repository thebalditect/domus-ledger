from api.src.domus_ledger_api.modules.ledger.household.use_cases.abstractions.uow.abstract_household_uow import (
    AbstractHouseholdUnitOfWork,
)
from api.src.domus_ledger_api.modules.ledger.household.use_cases.create_household.command import (
    CreateHouseholdCommand,
)
from api.src.domus_ledger_api.shared_kernel.domain.result import Result
from api.src.domus_ledger_api.modules.ledger.household.domain.entities.errors import (
    HouseholdErrors,
)


class CreateHouseholdCommandHandler:

    def __init__(self, uow: AbstractHouseholdUnitOfWork) -> None:
        self.uow = uow

    async def handle(self, command: CreateHouseholdCommand) -> Result[None]:

        async with self.uow:

            get_household_result = await self.uow.respository.get_household()

            if get_household_result.is_success:
                return Result[None].failure(HouseholdErrors.household_already_exists())

            if get_household_result.is_failure and get_household_result.errors == [
                HouseholdErrors.multiple_household_found()
            ]:
                return Result[None].failure(get_household_result.errors)

            ## Create household
            return Result[None].success(None)
