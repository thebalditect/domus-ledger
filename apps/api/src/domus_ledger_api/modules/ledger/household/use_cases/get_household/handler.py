from api.src.domus_ledger_api.modules.ledger.household.domain.repositories.abtract_household_repository import (
    AbstractHouseholdRepository,
)
from api.src.domus_ledger_api.modules.ledger.household.use_cases.get_household.response import (
    QueryResponse,
)
from api.src.domus_ledger_api.shared_kernel.domain.result import Result


class GetHouseholdQueryHandler:

    def __init__(self, repository: AbstractHouseholdRepository) -> None:
        self.repository = repository

    async def handle(self) -> Result[QueryResponse]:

        get_household_result = await self.repository.get_household()

        if get_household_result.is_success:
            query_response = QueryResponse(
                get_household_result.value.name, get_household_result.value.description
            )
            return Result[QueryResponse].success(query_response)

        return Result[QueryResponse].failure(get_household_result.errors)
