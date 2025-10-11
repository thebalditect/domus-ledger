from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


async def create_session_factory(database_url: str) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(database_url, echo=True)
    return async_sessionmaker(engine, expire_on_commit=True)
