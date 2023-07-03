from sqlmodel import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from ..settings import settings
from app.models import bill, account
from app.lib.utils.log import logger


engine = create_async_engine(settings.db_connection)
SessionFactory = sessionmaker(
    autocommit=False,
    autoflush=False,
    future=True,
    bind=engine,
    class_=AsyncSession,  # type: ignore
)


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
        session_factory=SessionFactory,
        table_model_metadata: tuple[MetaData, ...] = (
            bill.bills_metadata,
            account.accounts_metadata,
        ),
    ):
        self._session_factory = session_factory
        self.table_model_metadata = table_model_metadata

    async def __aenter__(self) -> AsyncSession:
        self.session = self._session_factory()
        return self.session

    async def __aexit__(self, exc_type, exc_value, traceback):
        return await self.session.close()

    async def create_tables(self):
        async with engine.begin() as conn:
            for metadata in self.table_model_metadata:
                try:
                    await conn.run_sync(metadata.create_all)
                except Exception as e:
                    # Handle or log the exception accordingly
                    logger(f"Error creating tables: {e}")

    async def close(self):
        """Close the database connection."""
        return await engine.dispose()
