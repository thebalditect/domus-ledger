import uuid
from dataclasses import dataclass
from typing import Any
from uuid import UUID
from datetime import datetime, timezone


@dataclass
class BaseEntity:
    id: UUID
    created_on: datetime
    updated_on: datetime

    def __init__(self, created_on: datetime | None, updated_on: datetime | None):
        self.id = uuid.uuid4()

        if created_on is None:
            self.created_on = datetime.now(timezone.utc)
        else:
            self.created_on = created_on

        if updated_on is None:
            self.updated_on = self.created_on
        else:
            self.updated_on = updated_on

    def __eq__(self, other: Any) -> bool:

        if not isinstance(other, BaseEntity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
