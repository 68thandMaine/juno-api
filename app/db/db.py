import os
from sys import modules

from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine

from sqlalchemy.orm import sessionmaker
from app.core.config import settings

db_connection_str = settings.db_connection

if 'pytest' in modules:
    db_connection_str = settings.db_test_connection

engine = AsyncEngine(create_engine(settings.db_connection, echo=True, future=True))


async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
