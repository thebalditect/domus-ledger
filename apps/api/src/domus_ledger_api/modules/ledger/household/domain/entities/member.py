from __future__ import annotations
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, List
from uuid import UUID
from api.src.domus_ledger_api.modules.ledger.household.domain.entities.errors import (
    HouseholdErrors,
)
from api.src.domus_ledger_api.modules.ledger.household.domain.entities.member_role import (
    MemberRole,
)
from api.src.domus_ledger_api.shared_kernel.domain.base_entity import BaseEntity
from api.src.domus_ledger_api.shared_kernel.domain.result import Result
from api.src.domus_ledger_api.shared_kernel.domain.error import Error


@dataclass
class Member(BaseEntity):
    name: str
    email: str
    birth_date: datetime
    gender: str
    avatar: bytes
    role: MemberRole | None
    household_id: UUID

    def __init__(
        self,
        name: str,
        email: str,
        birth_date: datetime,
        gender: str,
        avatar: bytes,
        role: MemberRole | None,
        household_id: UUID,
    ):

        super().__init__()
        self.name = name
        self.email = email
        self.birth_date = birth_date
        self.gender = gender
        self.avatar = avatar
        self.household_id = household_id

        if role is None:
            self.role = MemberRole.REGULAR
        else:
            self.role = role

    @classmethod
    def create(
        cls,
        name: str,
        email: str,
        birth_date: datetime,
        gender: str,
        avatar: bytes,
        role: MemberRole | None,
        household_id: UUID,
    ) -> Result[Member]:

        errors: List[Error] = []

        validators: tuple[Callable[[], List[Error]], ...] = (
            lambda: cls._validate_name(name),
            lambda: cls._validate_email(email),
            lambda: cls._validate_age(birth_date),
            lambda: cls._validate_gender(gender),
            lambda: cls._validate_avatar(avatar),
            lambda: cls._validate_household_id(household_id),
        )

        for validate in validators:
            errors.extend(validate())

        if len(errors) > 0:
            return Result[Member].failure(errors=errors)

        member = Member(
            name=name,
            email=email,
            birth_date=birth_date,
            gender=gender,
            avatar=avatar,
            role=role,
            household_id=household_id,
        )
        return Result[Member].success(member)

    @staticmethod
    def _validate_name(name: str) -> List[Error]:
        if not name or name.isspace():
            return [HouseholdErrors.invalid_name()]

        return []

    @staticmethod
    def _validate_email(email: str) -> List[Error]:
        EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.fullmatch(EMAIL_REGEX, email) is None:
            return [HouseholdErrors.invalid_email()]

        return []

    @staticmethod
    def _validate_gender(gender: str) -> List[Error]:
        if not gender or gender.isspace():
            return [HouseholdErrors.invalid_gender()]

        return []

    @staticmethod
    def _validate_avatar(avatar: bytes) -> List[Error]:
        if (
            not avatar
            or len(avatar) == 0
            or not avatar.startswith(b"\x89PNG\r\n\x1a\n")
        ):
            return [HouseholdErrors.invalid_image_format()]

        return []

    @staticmethod
    def _validate_age(birth_date: datetime) -> List[Error]:
        if birth_date.date() > datetime.now().date():
            error = HouseholdErrors.unborn_member()
            return [error]

        AGE_THRESHOLD: int = 16

        reference_date = datetime.today()

        age = reference_date.year - birth_date.year

        # Adjust if birthday hasn't occurred this year yet
        if (reference_date.month, reference_date.day) < (
            birth_date.month,
            birth_date.day,
        ):
            age -= 1

        if age < AGE_THRESHOLD and birth_date.date() <= datetime.now().date():

            error = HouseholdErrors.member_younger_than_sixteen_years_of_age()
            return [error]

        return []

    @staticmethod
    def _calculate_age(birth_date: datetime) -> int:

        reference_date = datetime.today()

        age = reference_date.year - birth_date.year

        # Adjust if birthday hasn't occurred this year yet
        if (reference_date.month, reference_date.day) < (
            birth_date.month,
            birth_date.day,
        ):
            age -= 1

        return age

    @staticmethod
    def _validate_household_id(household_id: UUID) -> List[Error]:

        try:
            household_id = UUID(str(household_id), version=4)
            return []
        except ValueError:
            return [HouseholdErrors.invalid_uuid("household_id", "UUID")]
