from domus_ledger_api.modules.ledger.household.domain.entities.member import (
    Member,
)
from domus_ledger_api.modules.ledger.household.infrastructure.models.memberorm import (
    MemberORM,
)


class MemberMapper:

    @classmethod
    def to_orm(cls, member: Member) -> MemberORM:

        member_orm = MemberORM(
            id=member.id,
            name=member.name,
            email=member.email,
            birth_date=member.birth_date,
            gender=member.gender,
            avatar=member.avatar,
            role=member.role,
            household_id=member.household_id,
            created_on=member.created_on,
            updated_on=member.updated_on,
        )

        return member_orm

    @classmethod
    def to_domain(cls, member_orm: MemberORM) -> Member:
        member_result = Member.create(
            name=member_orm.name,
            email=member_orm.email,
            birth_date=member_orm.birth_date,
            gender=member_orm.gender,
            avatar=member_orm.avatar,
            role=member_orm.role,
            household_id=member_orm.household_id,
        )
        if member_result.is_failure:
            error_message = ""
            for error in member_result.errors:
                error_message = error_message + error.description + "\n"
            raise ValueError(error_message)

        member = member_result.value
        object.__setattr__(member, "id", member_orm.id)
        object.__setattr__(member, "created_on", member_orm.created_on)
        object.__setattr__(member, "updated_on", member_orm.updated_on)
        return member
