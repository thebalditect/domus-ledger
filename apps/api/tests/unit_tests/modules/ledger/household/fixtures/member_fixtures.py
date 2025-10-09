from dataclasses import dataclass
from datetime import datetime
from typing import List
import pytest

from api.src.domus_ledger_api.modules.ledger.household.member import Member
from api.src.domus_ledger_api.modules.ledger.household.member_role import MemberRole


@dataclass
class MemberData:
    name: str
    email: str
    birth_date: datetime
    gender: str
    avatar: bytes
    role: MemberRole


@pytest.fixture
def valid_member_data() -> MemberData:

    return MemberData(
        name="John Doe",
        email="john.doe@test.com",
        birth_date=datetime(1980, 1, 1),
        gender="Male",
        avatar=b"\x89PNG\r\n\x1a\n" + b"somebytes",
        role=MemberRole.ADMINISTRATOR,
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
    ).value
