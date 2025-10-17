from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List
import uuid
import pytest

from domus_ledger_api.modules.ledger.household.domain.entities.member import (
    Member,
)
from domus_ledger_api.modules.ledger.household.domain.entities.member_role import (
    MemberRole,
)
from domus_ledger_api.modules.ledger.household.infrastructure.models.memberorm import (
    MemberORM,
)


@dataclass
class MemberData:
    name: str
    email: str
    birth_date: datetime
    gender: str
    avatar: bytes
    role: MemberRole
    household_id: uuid.UUID


@pytest.fixture
def valid_member_data() -> MemberData:

    return MemberData(
        name="John Doe",
        email="john.doe@test.com",
        birth_date=datetime(1980, 1, 1),
        gender="Male",
        avatar=b"\x89PNG\r\n\x1a\n" + b"somebytes",
        role=MemberRole.ADMINISTRATOR,
        household_id=uuid.uuid4(),
    )


@pytest.fixture
def invalid_member_name() -> List[str]:
    return ["", " "]


@pytest.fixture
def invalid_member_email() -> List[str]:
    return ["", " ", "invalid email", "invalid@1", ".com"]


@pytest.fixture
def invalid_member_gender() -> List[str]:
    return ["", " "]


@pytest.fixture
def invalid_member_avatar() -> List[bytes]:
    return [b"", b" "]


@pytest.fixture
def valid_member(valid_member_data: MemberData) -> Member:
    return Member.create(
        valid_member_data.name,
        valid_member_data.email,
        valid_member_data.birth_date,
        valid_member_data.gender,
        valid_member_data.avatar,
        valid_member_data.role,
        valid_member_data.household_id,
    ).value


@pytest.fixture
def valid_member_orm(valid_member: Member) -> MemberORM:

    return MemberORM(
        id=valid_member.id,
        name=valid_member.name,
        email=valid_member.email,
        gender=valid_member.gender,
        birth_date=valid_member.birth_date,
        avatar=valid_member.avatar,
        role=valid_member.role,
        household_id=valid_member.household_id,
        created_on=datetime.now(timezone.utc),
        updated_on=datetime.now(timezone.utc),
    )
