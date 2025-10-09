from dataclasses import dataclass, field
from api.src.domus_ledger_api.shared_kernel.domain.base_entity import BaseEntity


@dataclass
class SampleEntity(BaseEntity):

    name: str = field(init=True)

    def __init__(self, name: str):
        super().__init__()
        self.name = name


@dataclass
class DifferentSampleEntity(BaseEntity):
    name: str = field(init=True)

    def __init__(self, name: str):
        super().__init__()
        self.name = name


# Tests


def test_entity_has_unique_id() -> None:
    e1 = SampleEntity("foo")
    e2 = SampleEntity("bar")
    assert e1.id != e2.id


def test_entity_equality_based_on_id() -> None:
    e1 = SampleEntity("foo")
    e2 = e1

    assert e1.id == e2.id


def test_two_entity_subtypes_are_not_equal() -> None:
    e1 = SampleEntity("foo")
    e2 = DifferentSampleEntity("foo")

    assert e1 != e2


def test_entity_has_id_and_createdon() -> None:
    e1 = SampleEntity("foo")

    assert e1.id is not None
    assert e1.created_on is not None
