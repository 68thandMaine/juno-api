from sqlmodel import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.core.config import settings
from app.models.all import Bill
from app.lib.utils.log import logger


engine = AsyncEngine(create_engine(settings.db_connection, echo=True, future=True))
SessionFactory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class JunoTables:
    """The Juno Database management class which can be used
    with an async context manager to create database sessions."""

    __slots__ = (
        "_session_factory",
        "session",
        "table_model_metadata",
    )

    def __init__(
        self,
        session_factory=SessionFactory
        # table_model_metadata: tuple[MetaData, ...] = (bill.juno_metadata,),
    ):
        logger(settings.db_connection)
        self._session_factory = {}
        # self.table_model_metadata = table_model_metadata

    # async def __aenter__(self) -> AsyncSession:
    #     self.session = self._session_factory()
    #     return self.session

    # async def __aexit__(self, exc_type, exc_value, traceback):
    #     return await self.session.close()

    async def create_tables(self):
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
            # for metadata in self.table_model_metadata:
            #     try:
            #         await conn.run_sync(metadata.create_all)
            #     except Exception as e:
            #         # Handle or log the exception accordingly
            #         logger(f"Error creating tables: {e}")

    async def drop_tables(self):
        async with engine.begin() as conn:
            for metadata in self.table_model_metadata:
                # Need to synchronously create tables to avoid asyncpg error
                await conn.run_sync(metadata.drop_all)

    async def close(self):
        """Close the database connection."""
        return await engine.dispose()
