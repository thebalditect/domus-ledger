from api.src.domus_ledger_api.modules.ledger.household.domain.household import Household
from api.src.domus_ledger_api.modules.ledger.household.infrastructure.models.householdorm import (
    HouseholdORM,
)
from api.src.domus_ledger_api.modules.ledger.household.infrastructure.mappers.member_mapper import (
    MemberMapper,
)


class HouseholdMapper:

    @classmethod
    def to_orm(cls, household: Household) -> HouseholdORM:

        members = [MemberMapper.to_orm(member) for member in household.members]

        householdorm = HouseholdORM(
            id=household.id,
            name=household.name,
            description=household.description,
            members=members,
        )
        return householdorm

    @classmethod
    def to_domain(cls, household_orm: HouseholdORM) -> Household:

        create_result = Household.create(
            name=household_orm.name, description=household_orm.description
        )

        if create_result.is_failure:
            error_message = ""
            for error in create_result.errors:
                error_message = error_message + error.description + "\n"

            raise ValueError(error_message)

        household = create_result.value

        object.__setattr__(household, "id", household_orm.id)
        return household
