import uuid
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, String, DateTime, LargeBinary, Enum, ForeignKey
from datetime import datetime
from api.src.domus_ledger_api.modules.ledger.household.infrastructure.models.base import (
    Base,
)
from api.src.domus_ledger_api.modules.ledger.household.domain.entities.member_role import (
    MemberRole,
)


if TYPE_CHECKING:
    from api.src.domus_ledger_api.modules.ledger.household.infrastructure.models.householdorm import (
        HouseholdORM,
    )


class MemberORM(Base):

    __tablename__ = "members"

    id: Mapped[uuid.UUID] = mapped_column(
        name="id", type_=UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(name="name", type_=String(50), nullable=False)
    email: Mapped[str] = mapped_column(name="email", type_=String(50), nullable=False)
    birth_date: Mapped[datetime] = mapped_column(
        name="birth_date", type_=DateTime, nullable=False
    )
    gender: Mapped[str] = mapped_column(name="gender", type_=String(10), nullable=False)
    avatar: Mapped[bytes] = mapped_column(
        name="avatar", type_=LargeBinary, nullable=False
    )
    role: Mapped[MemberRole] = mapped_column(
        name="role",
        type_=Enum(MemberRole, name="member_role_enum", create_type=False),
        nullable=False,
    )
    household_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("households.id"), nullable=False
    )
    household: Mapped["HouseholdORM"] = relationship(
        "HouseholdORM", back_populates="members"
    )
    created_on: Mapped[DateTime] = mapped_column(
        name="created_on", type_=DateTime, nullable=False
    )
    updated_on: Mapped[datetime] = mapped_column(
        "updated_on", type_=DateTime, nullable=False
    )
