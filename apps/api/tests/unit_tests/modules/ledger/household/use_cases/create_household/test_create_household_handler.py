import pytest
from unittest.mock import AsyncMock

from api.src.domus_ledger_api.modules.ledger.household.domain.entities.errors import (
    HouseholdErrors,
)
from api.src.domus_ledger_api.modules.ledger.household.domain.entities.household import (
    Household,
)
from api.src.domus_ledger_api.modules.ledger.household.domain.repositories.abtract_household_repository import (
    AbstractHouseholdRepository,
)
from api.src.domus_ledger_api.modules.ledger.household.use_cases.abstractions.uow.abstract_household_uow import (
    AbstractHouseholdUnitOfWork,
)
from api.src.domus_ledger_api.modules.ledger.household.use_cases.create_household.command import (
    CreateHouseholdCommand,
)
from api.src.domus_ledger_api.modules.ledger.household.use_cases.create_household.handler import (
    CreateHouseholdCommandHandler,
)
from api.src.domus_ledger_api.shared_kernel.domain.result import Result


@pytest.mark.asyncio
async def test_handle_should_return_success_result() -> None:

    household_uow = AsyncMock(spec=AbstractHouseholdUnitOfWork)
    household_uow.repository = AsyncMock(spec=AbstractHouseholdRepository)
    household_uow.repository.get_household.return_value = Result[Household].failure(
        HouseholdErrors.household_not_found()
    )
    household_uow.repository.create_household.return_value = Result[None].success(None)

    create_command = CreateHouseholdCommand(name="test", description="test")

    handler = CreateHouseholdCommandHandler(household_uow)

    result = await handler.handle(create_command)

    assert result.is_success
    household_uow.repository.create_household.assert_called_once()


@pytest.mark.asyncio
async def test_handle_should_return_failure_result_when_household_already_exist(
    valid_household: Household,
) -> None:

    household_uow = AsyncMock(spec=AbstractHouseholdUnitOfWork)
    household_uow.repository = AsyncMock(spec=AbstractHouseholdRepository)
    household_uow.repository.get_household.return_value = Result[Household].success(
        valid_household
    )
    household_uow.repository.create_household.return_value = Result[None].failure(
        HouseholdErrors.household_already_exists()
    )

    create_command = CreateHouseholdCommand(
        valid_household.name, valid_household.description
    )
    handler = CreateHouseholdCommandHandler(household_uow)
    result = await handler.handle(create_command)

    assert result.is_failure
    assert result.errors == [HouseholdErrors.household_already_exists()]


@pytest.mark.asyncio
async def test_handle_should_return_failure_when_multiple_household_exist(
    valid_household: Household,
) -> None:
    household_uow = AsyncMock(spec=AbstractHouseholdUnitOfWork)
    household_uow.repository = AsyncMock(spec=AbstractHouseholdRepository)
    household_uow.repository.get_household.return_value = Result[Household].failure(
        HouseholdErrors.multiple_household_found()
    )
    household_uow.repository.create_household.return_value = Result[None].failure(
        HouseholdErrors.multiple_household_found()
    )

    create_command = CreateHouseholdCommand(
        valid_household.name, valid_household.description
    )
    handler = CreateHouseholdCommandHandler(household_uow)
    result = await handler.handle(create_command)

    assert result.is_failure
    assert result.errors == [HouseholdErrors.multiple_household_found()]


@pytest.mark.asyncio
async def test_handle_should_return_failure_result_for_domain_validation_failures() -> (
    None
):
    household_uow = AsyncMock(spec=AbstractHouseholdUnitOfWork)
    household_uow.repository = AsyncMock(spec=AbstractHouseholdRepository)
    household_uow.repository.get_household.return_value = Result[Household].failure(
        HouseholdErrors.household_not_found()
    )
    household_uow.repository.create_household.return_value = Result[None].success(None)

    create_command = CreateHouseholdCommand(name="", description="")

    handler = CreateHouseholdCommandHandler(household_uow)

    result = await handler.handle(create_command)

    expected_errors = [
        HouseholdErrors.invalid_name(),
        HouseholdErrors.invalid_description(),
    ]
    assert result.is_failure
    assert result.errors == expected_errors
