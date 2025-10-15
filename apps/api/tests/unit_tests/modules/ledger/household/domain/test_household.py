from typing import List
from api.src.domus_ledger_api.modules.ledger.household.domain.entities.errors import (
    HouseholdErrors,
)
from api.src.domus_ledger_api.modules.ledger.household.domain.entities.household import (
    Household,
)
from api.src.domus_ledger_api.modules.ledger.household.domain.entities.member import (
    Member,
)
from api.tests.unit_tests.modules.ledger.household.fixtures.household_fixtures import (
    HouseholdData,
)


def test_create_should_return_success_result(
    valid_household_data: HouseholdData,
) -> None:

    result = Household.create(
        name=valid_household_data.name, description=valid_household_data.description
    )
    assert result.is_success
    assert not result.is_failure
    assert result.value.name == valid_household_data.name
    assert result.value.description == valid_household_data.description
    assert result.value.created_on is not None
    assert result.value.updated_on is not None


def test_create_should_return_failure_result_for_invalid_household_name(
    valid_household_data: HouseholdData, invalid_household_name: List[str]
) -> None:

    for name in invalid_household_name:
        result = Household.create(name, valid_household_data.description)

        assert result.is_failure
        assert not result.is_success
        assert len(result.errors) == 1
        assert result.errors[0] == HouseholdErrors.invalid_name()


def test_create_should_return_failure_result_for_invalid_household_description(
    valid_household_data: HouseholdData, invalid_household_description: List[str]
) -> None:

    for description in invalid_household_description:
        result = Household.create(valid_household_data.name, description)

        assert result.is_failure
        assert not result.is_success
        assert len(result.errors) == 1
        assert result.errors[0] == HouseholdErrors.invalid_description()


def test_create_should_return_all_validation_errors_with_failure_result(
    invalid_household_data: HouseholdData,
) -> None:

    result = Household.create(
        invalid_household_data.name, invalid_household_data.description
    )

    assert result.is_failure
    assert not result.is_success
    assert len(result.errors) == 2

    expected_errors = [
        HouseholdErrors.invalid_name(),
        HouseholdErrors.invalid_description(),
    ]

    assert result.errors == expected_errors


def test_add_member_should_return_success_result(
    valid_household: Household, valid_member: Member
) -> None:

    household = valid_household
    member = valid_member

    result = household.add_member(member)

    assert result.is_success
    assert not result.is_failure
    assert result.value is None


def test_add_member_should_return_failure_result_for_already_added_member(
    valid_household: Household, valid_member: Member
) -> None:

    household = valid_household
    member = valid_member

    household.add_member(member)
    result = household.add_member(member)

    assert result.is_failure
    assert not result.is_success
    assert len(result.errors) == 1
    assert result.errors[0] == HouseholdErrors.member_already_added_to_household(
        member.email
    )


def test_remove_member_should_return_success_result(
    valid_household: Household, valid_member: Member
) -> None:

    household = valid_household
    member = valid_member

    add_member_result = household.add_member(member)

    assert add_member_result.is_success
    assert len(household.members) == 1

    remove_member_result = household.remove_member(member)

    assert remove_member_result.is_success
    assert not remove_member_result.is_failure


def test_remove_user_should_return_failure_result_while_removing_non_existent_member(
    valid_household: Household, valid_member: Member
) -> None:

    household = valid_household
    member = valid_member

    result = household.remove_member(member)

    assert result.is_failure
    assert not result.is_success
    assert len(result.errors) == 1
    assert result.errors[0] == HouseholdErrors.member_does_not_exist_in_household(
        member.email
    )
