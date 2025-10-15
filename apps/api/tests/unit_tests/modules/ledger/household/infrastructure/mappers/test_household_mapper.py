import uuid

import pytest
from api.src.domus_ledger_api.modules.ledger.household.domain.entities.household import (
    Household,
)
from api.src.domus_ledger_api.modules.ledger.household.infrastructure.mappers.household_mapper import (
    HouseholdMapper,
)

from api.src.domus_ledger_api.modules.ledger.household.infrastructure.models import (
    HouseholdORM,
)


def test_to_orm_should_return_household_orm_instance(
    valid_household: Household,
) -> None:
    household = valid_household

    household_orm = HouseholdMapper.to_orm(household)

    assert household_orm.id == household.id
    assert household_orm.name == household.name
    assert household_orm.description == household.description
    assert len(household_orm.members) == len(household.members)


def test_to_domain_should_return_household_domain_entity_instance() -> None:
    household_orm = HouseholdORM(
        id=uuid.uuid4(),
        name="The balditect household",
        description="The household of the balditect",
    )

    household = HouseholdMapper.to_domain(household_orm)

    assert household.id == household_orm.id
    assert household.name == household_orm.name
    assert household.description == household_orm.description


def test_to_domain_should_throw_value_error_for_incorrect_household_orm_instance() -> (
    None
):
    household_orm = HouseholdORM(
        id=uuid.uuid4(),
        name="",
        description="",
    )
    expected_error_message = (
        "name cannot be empty or whitespace."
        + "\n"
        + "description cannot be empty or whitespace."
    )
    with pytest.raises(ValueError, match=expected_error_message):
        HouseholdMapper.to_domain(household_orm)
