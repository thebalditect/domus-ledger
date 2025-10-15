from datetime import datetime
from typing import List, TYPE_CHECKING
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, DateTime, String
from api.src.domus_ledger_api.modules.ledger.household.infrastructure.models.base import (
    Base,
)

if TYPE_CHECKING:
    from api.src.domus_ledger_api.modules.ledger.household.infrastructure.models.memberorm import (
        MemberORM,
    )


class HouseholdORM(Base):
    __tablename__ = "households"

    id: Mapped[uuid.UUID] = mapped_column(
        name="id", type_=UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(name="name", type_=String(50), nullable=False)
    description: Mapped[str] = mapped_column(
        name="description", type_=String(200), nullable=False
    )
    members: Mapped[List["MemberORM"]] = relationship(
        "MemberORM",
        back_populates="household",
        cascade="all, delete-orphan",
        lazy="joined",
    )
    created_on: Mapped[datetime] = mapped_column(
        name="created_on", type_=DateTime, nullable=False
    )
    updated_on: Mapped[datetime] = mapped_column(
        name="updated_on", type_=DateTime, nullable=False
    )
