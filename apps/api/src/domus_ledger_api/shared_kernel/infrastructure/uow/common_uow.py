from __future__ import annotations
from types import TracebackType
from typing import Self
from domus_ledger_api.shared_kernel.application.uow.abstract_uow import (
    AbstractUnitOfWork,
)
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class CommonUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def __aenter__(self) -> Self:
        """Starts a new session"""
        self._session = self._session_factory()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:

        if exc_type is not None:
            await self.rollback()

        if self._session:
            await self._session.close()

    async def commit(self) -> None:

        if not self._session:
            raise RuntimeError("No active session found.")

        try:
            await self._session.commit()

        except Exception as e:
            await self.rollback()
            raise e

    async def rollback(self) -> None:

        if self._session:
            await self._session.rollback()
