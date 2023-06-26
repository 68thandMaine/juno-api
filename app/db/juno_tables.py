import sqlalchemy
from sqlmodel import MetaData
from sqlalchemy.ext.asyncio import create_async_engine
from app.settings import settings
from app.models import bills

engine = create_async_engine(settings.db_connection)


class JunoTables:
    """The Juno Database management class which can be used
    with an async context manager to create database sessions."""

    def __init__(
        self,
        table_model_metadata: tuple[MetaData, ...] = (
          tuple[MetaData, ...] = (bills.metadata,)
        ),
    ):
        self.table_model_metadata: table_model_metadata

    async def create_tables(self):
        async with engine.connect() as conn:
            for metadata in self.table_model_metadata:
                try:
                    await conn.run_sync(metadata.create_all)
                except Exception as e:
                    # Handle or log the exception accordingly
                    print(f"Error creating tables: {e}")
