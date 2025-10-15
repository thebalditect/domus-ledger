from dataclasses import dataclass
from typing import List
import pytest

from api.src.domus_ledger_api.modules.ledger.household.domain.entities.household import (
    Household,
)


@dataclass
class HouseholdData:
    name: str
    description: str


@pytest.fixture
def valid_household_data() -> HouseholdData:
    return HouseholdData(
        name="The Balditect Household",
        description="This is the house hold of the Balditect.",
    )


@pytest.fixture
def invalid_household_name() -> List[str]:
    return ["", " "]


@pytest.fixture
def invalid_household_description() -> List[str]:
    return ["", " "]


@pytest.fixture
def invalid_household_data() -> HouseholdData:
    return HouseholdData(name="", description="")


@pytest.fixture
def valid_household(valid_household_data: HouseholdData) -> Household:
    return Household.create(
        valid_household_data.name, valid_household_data.description
    ).value
