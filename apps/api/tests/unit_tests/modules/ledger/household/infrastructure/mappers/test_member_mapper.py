import pytest
from api.src.domus_ledger_api.modules.ledger.household.domain.entities.member import (
    Member,
)
from api.src.domus_ledger_api.modules.ledger.household.infrastructure.mappers.member_mapper import (
    MemberMapper,
)
from api.src.domus_ledger_api.modules.ledger.household.infrastructure.models import (
    MemberORM,
)


def test_to_orm_should_return_member_orm_instance(valid_member: Member) -> None:
    member = valid_member

    member_orm = MemberMapper.to_orm(member)

    assert member_orm.id == member.id
    assert member_orm.name == member.name
    assert member_orm.email == member.email
    assert member_orm.birth_date == member.birth_date
    assert member_orm.gender == member.gender
    assert member_orm.avatar == member.avatar
    assert member_orm.role == member.role
    assert member_orm.household_id == member.household_id
    assert member_orm.created_on == member.created_on
    assert member_orm.updated_on == member.updated_on


def test_to_domain_should_return_member_entity_instance(
    valid_member_orm: MemberORM,
) -> None:
    member_orm = valid_member_orm

    member = MemberMapper.to_domain(member_orm)

    assert member.id == valid_member_orm.id
    assert member.name == member_orm.name
    assert member.created_on == member_orm.created_on
    assert member.updated_on == member_orm.updated_on


def test_to_domain_should_raise_value_error_for_invalid_member_orm_instance(
    valid_member_orm: MemberORM,
) -> None:
    invalid_member_orm = valid_member_orm
    invalid_member_orm.name = ""

    expected_error_message = "name cannot be empty or whitespace." + "\n"

    with pytest.raises(ValueError, match=expected_error_message):
        MemberMapper.to_domain(invalid_member_orm)
