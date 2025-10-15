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
from api.src.domus_ledger_api.modules.ledger.household.domain.entities.household import (
    Household,
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
            household_domain_create_result = Household.create(
                command.name, command.description
            )

            if household_domain_create_result.is_failure:
                return Result[None].failure(household_domain_create_result.errors)

            async with self.uow:
                persist_result = self.uow.respository.create_household(
                    household_domain_create_result.value
                )

                if persist_result.is_failure:
                    return Result[None].failure(persist_result.errors)

            return Result[None].success(None)
