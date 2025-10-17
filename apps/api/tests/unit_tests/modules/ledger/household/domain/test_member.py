from datetime import datetime, timedelta
from typing import List
from domus_ledger_api.modules.ledger.household.domain.entities.errors import (
    HouseholdErrors,
)
from domus_ledger_api.modules.ledger.household.domain.entities.member import (
    Member,
)
from domus_ledger_api.modules.ledger.household.domain.entities.member_role import (
    MemberRole,
)
from tests.unit_tests.modules.ledger.household.fixtures.member_fixtures import (
    MemberData,
)


def test_create_should_return_success_result(valid_member_data: MemberData) -> None:

    result = Member.create(
        valid_member_data.name,
        valid_member_data.email,
        valid_member_data.birth_date,
        valid_member_data.gender,
        valid_member_data.avatar,
        valid_member_data.role,
        valid_member_data.household_id,
    )

    assert result.is_success
    assert not result.is_failure

    member = result.value
    assert member.name == valid_member_data.name
    assert member.email == valid_member_data.email
    assert member.birth_date == valid_member_data.birth_date
    assert member.gender == valid_member_data.gender
    assert member.avatar == valid_member_data.avatar
    assert member.role == valid_member_data.role
    assert member.id is not None
    assert member.household_id == valid_member_data.household_id
    assert member.created_on is not None
    assert member.updated_on is not None


def test_for_invalid_name_create_should_return_failure_result(
    valid_member_data: MemberData, invalid_member_name: List[str]
) -> None:

    for name in invalid_member_name:
        result = Member.create(
            name,
            valid_member_data.email,
            valid_member_data.birth_date,
            valid_member_data.gender,
            valid_member_data.avatar,
            valid_member_data.role,
            valid_member_data.household_id,
        )
        assert result.is_failure
        assert not result.is_success
        assert len(result.errors) == 1
        assert result.errors[0] == HouseholdErrors.invalid_name()


def test_for_invalid_email_create_should_return_failure_result(
    valid_member_data: MemberData, invalid_member_email: List[str]
) -> None:

    for email in invalid_member_email:
        result = Member.create(
            valid_member_data.name,
            email,
            valid_member_data.birth_date,
            valid_member_data.gender,
            valid_member_data.avatar,
            valid_member_data.role,
            valid_member_data.household_id,
        )
        assert result.is_failure
        assert not result.is_success
        assert len(result.errors) == 1
        assert result.errors[0] == HouseholdErrors.invalid_email()


def test_for_invalid_gender_create_should_return_failure_result(
    valid_member_data: MemberData, invalid_member_gender: List[str]
) -> None:
    for gender in invalid_member_gender:
        result = Member.create(
            valid_member_data.name,
            valid_member_data.email,
            valid_member_data.birth_date,
            gender,
            valid_member_data.avatar,
            valid_member_data.role,
            valid_member_data.household_id,
        )
        assert result.is_failure
        assert not result.is_success
        assert len(result.errors) == 1
        assert result.errors[0] == HouseholdErrors.invalid_gender()


def test_for_non_png_type_avatar_create_should_return_failure_result(
    valid_member_data: MemberData, invalid_member_avatar: List[bytes]
) -> None:
    for avatar in invalid_member_avatar:
        result = Member.create(
            valid_member_data.name,
            valid_member_data.email,
            valid_member_data.birth_date,
            valid_member_data.gender,
            avatar,
            valid_member_data.role,
            valid_member_data.household_id,
        )
        assert result.is_failure
        assert not result.is_success
        assert len(result.errors) == 1
        assert result.errors[0] == HouseholdErrors.invalid_image_format()


def test_if_not_specified_default_member_role_should_be_regular(
    valid_member_data: MemberData,
) -> None:
    result = Member.create(
        valid_member_data.name,
        valid_member_data.email,
        valid_member_data.birth_date,
        valid_member_data.gender,
        valid_member_data.avatar,
        None,
        valid_member_data.household_id,
    )

    assert result.is_success
    assert not result.is_failure

    member = result.value
    assert member.name == valid_member_data.name
    assert member.email == valid_member_data.email
    assert member.birth_date == valid_member_data.birth_date
    assert member.gender == valid_member_data.gender
    assert member.avatar == valid_member_data.avatar
    assert member.role == MemberRole.REGULAR
    assert member.id is not None


def test_create_should_return_failure_result_while_creating_unborn_member(
    valid_member_data: MemberData,
) -> None:

    birth_date = datetime(2100, 1, 1)
    result = Member.create(
        valid_member_data.name,
        valid_member_data.email,
        birth_date,
        valid_member_data.gender,
        valid_member_data.avatar,
        valid_member_data.role,
        valid_member_data.household_id,
    )

    assert result.is_failure
    assert not result.is_success
    assert len(result.errors) == 1
    assert result.errors[0] == HouseholdErrors.unborn_member()


def test_create_should_return_failure_result_while_creating_member_younger_than_sixteen_years(
    valid_member_data: MemberData,
) -> None:

    birth_date = datetime.now() - timedelta(days=39)
    result = Member.create(
        valid_member_data.name,
        valid_member_data.email,
        birth_date,
        valid_member_data.gender,
        valid_member_data.avatar,
        valid_member_data.role,
        valid_member_data.household_id,
    )

    assert result.is_failure
    assert not result.is_success
    assert len(result.errors) == 1
    assert (
        result.errors[0] == HouseholdErrors.member_younger_than_sixteen_years_of_age()
    )


def test_create_should_return_failure_result_for_invalid_household_id(
    valid_member_data: MemberData,
) -> None:
    result = Member.create(
        valid_member_data.name,
        valid_member_data.email,
        valid_member_data.birth_date,
        valid_member_data.gender,
        valid_member_data.avatar,
        valid_member_data.role,
        None,  # type: ignore
    )

    assert result.is_failure
    assert not result.is_success


def test_create_should_list_all_possible_errors_and_return_failure_result() -> None:

    result = Member.create(
        name="",
        email="",
        birth_date=datetime.now(),
        gender=" ",
        avatar=b"incorrect",
        role=MemberRole.REGULAR,
        household_id=None,  # type: ignore
    )

    assert result.is_failure
    assert not result.is_success
    assert len(result.errors) == 6

    expected_errors = [
        HouseholdErrors.invalid_name(),
        HouseholdErrors.invalid_email(),
        HouseholdErrors.member_younger_than_sixteen_years_of_age(),
        HouseholdErrors.invalid_gender(),
        HouseholdErrors.invalid_image_format(),
        HouseholdErrors.invalid_uuid("household_id", "UUID"),
    ]
    assert result.errors == expected_errors
