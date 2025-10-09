from __future__ import annotations
from dataclasses import dataclass
from api.src.domus_ledger_api.shared_kernel.domain.error_type import ErrorType


@dataclass(frozen=True)
class Error:
    code: str
    description: str
    error_type: ErrorType

    @staticmethod
    def failure(code: str, description: str) -> Error:
        return Error(code, description, ErrorType.FAILURE)

    @staticmethod
    def not_found(code: str, description: str) -> Error:
        return Error(code, description, ErrorType.NOT_FOUND)

    @staticmethod
    def conflict(code: str, description: str) -> Error:
        return Error(code, description, ErrorType.CONFLICT)

    @staticmethod
    def validation(code: str, description: str) -> Error:
        return Error(code, description, ErrorType.VALIDATION)
