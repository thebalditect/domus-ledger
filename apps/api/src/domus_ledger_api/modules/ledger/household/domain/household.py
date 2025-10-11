from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, List
from api.src.domus_ledger_api.modules.ledger.household.domain.errors import (
    HouseholdErrors,
)
from api.src.domus_ledger_api.modules.ledger.household.domain.member import Member
from api.src.domus_ledger_api.shared_kernel.domain.base_entity import BaseEntity
from api.src.domus_ledger_api.shared_kernel.domain.error import Error
from api.src.domus_ledger_api.shared_kernel.domain.result import Result


@dataclass()
class Household(BaseEntity):
    name: str
    description: str
    members: List[Member] = field(default_factory=list[Member])

    def __init__(self, name: str, description: str):

        super().__init__()
        self.name = name
        self.description = description
        self.members = []

    @classmethod
    def create(cls, name: str, description: str) -> Result[Household]:
        errors: List[Error] = []

        validators: tuple[Callable[[], List[Error]], ...] = (
            lambda: cls._validate_name(name),
            lambda: cls._validate_description(description),
        )

        for validate in validators:
            errors.extend(validate())

        if len(errors) > 0:
            return Result[Household].failure(errors)

        household = Household(name, description)
        return Result[Household].success(household)

    @staticmethod
    def _validate_name(name: str) -> List[Error]:

        if not name or name.isspace():
            return [HouseholdErrors.invalid_name()]

        return []

    @staticmethod
    def _validate_description(description: str) -> List[Error]:

        if not description or description.isspace():
            return [HouseholdErrors.invalid_description()]

        return []

    def add_member(self, member: Member) -> Result[None]:

        if any(
            existing_member.email.lower() == member.email.lower()
            for existing_member in self.members
        ):
            return Result[None].failure(
                [HouseholdErrors.member_already_added_to_household(member.email)]
            )

        self.members.append(member)
        return Result[None].success(None)

    def remove_member(self, member: Member) -> Result[None]:
        # Find the index of the member if it exists
        index = next(
            (
                i
                for i, existing_member in enumerate(self.members)
                if existing_member.email.lower() == member.email.lower()
            ),
            None,
        )

        if index is None:
            return Result[None].failure(
                [
                    HouseholdErrors.member_does_not_exist_in_household(
                        member.email.lower()
                    )
                ]
            )

        del self.members[index]
        return Result[None].success(None)
