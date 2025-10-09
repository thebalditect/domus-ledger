from enum import Enum


class ErrorType(str, Enum):
    FAILURE = "Failure"
    NOT_FOUND = "NotFound"
    CONFLICT = "Conflict"
    VALIDATION = "Validation"
    INVALID_STATE = "InvalidState"
