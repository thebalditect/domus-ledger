import pytest
from unittest.mock import AsyncMock
from api.src.domus_ledger_api.modules.ledger.household.domain.repositories.abtract_household_repository import (
    AbstractHouseholdRepository,
)
from api.src.domus_ledger_api.modules.ledger.household.domain.entities.household import (
    Household,
)
from api.src.domus_ledger_api.shared_kernel.domain.result import Result
from api.src.domus_ledger_api.modules.ledger.household.use_cases.get_household.handler import (
    GetHouseholdQueryHandler,
)
from api.src.domus_ledger_api.modules.ledger.household.use_cases.get_household.response import (
    QueryResponse,
)
from apps.api.src.domus_ledger_api.modules.ledger.household.domain.entities.errors import (
    HouseholdErrors,
)


@pytest.mark.asyncio
async def test_handle_should_return_success_result_with_query_response() -> None:

    household_repository = AsyncMock(spec=AbstractHouseholdRepository)

    household = Household.create("test", "test").value

    household_repository.get_household.return_value = Result[Household].success(
        household
    )

    handler = GetHouseholdQueryHandler(household_repository)
    result = await handler.handle()

    assert result.is_success
    household_retrieved: QueryResponse = result.value
    assert household_retrieved.name == household.name
    assert household.description == household.description


@pytest.mark.asyncio
async def test_handle_should_return_failure_result_when_no_household_is_found() -> None:

    household_repository = AsyncMock(spec=AbstractHouseholdRepository)
    household_repository.get_household.return_value = Result[Household].failure(
        HouseholdErrors.household_not_found()
    )

    handler = GetHouseholdQueryHandler(household_repository)
    result = await handler.handle()

    assert result.is_failure
    assert result.errors == [HouseholdErrors.household_not_found()]


@pytest.mark.asyncio
async def test_handler_should_return_failure_result_when_multiple_households_are_found() -> (
    None
):
    household_repository = AsyncMock(spec=AbstractHouseholdRepository)
    household_repository.get_household.return_value = Result[Household].failure(
        HouseholdErrors.multiple_household_found()
    )
    handler = GetHouseholdQueryHandler(household_repository)
    result = await handler.handle()

    assert result.is_failure
    assert result.errors == [HouseholdErrors.multiple_household_found()]
