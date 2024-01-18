from sqlmodel import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.core.config import settings


async_engine = create_async_engine(settings.db_connection, echo=True, future=True)
SessionFactory = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


class JunoDB:
    """The Juno Database management class which can be used
    with an async context manager to create database sessions."""

    __slots__ = (
        "_session_factory",
        "session",
    )

    def __init__(
        self,
        session_factory=SessionFactory,
    ) -> None:
        self._session_factory = session_factory

    async def __aenter__(self) -> AsyncSession:
        self.session = self._session_factory()
        return self.session

    async def __aexit__(self, exc_type, exc_value, traceback):
        return await self.session.close()

    async def create_tables(self):
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def drop_tables(self):
        async with async_engine.begin() as conn:
            for metadata in self.table_model_metadata:
                # Need to synchronously create tables to avoid asyncpg error
                await conn.run_sync(metadata.drop_all)

    async def close(self):
        """Close the database connection."""
        return await async_engine.dispose()


async def get_session() -> AsyncSession:
    async_session = SessionFactory()
    async with async_session as session:
        yield session
