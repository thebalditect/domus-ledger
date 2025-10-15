from enum import Enum


class MemberRole(str, Enum):
    ADMINISTRATOR = "ADMINISTRATOR"
    REGULAR = "REGULAR"
