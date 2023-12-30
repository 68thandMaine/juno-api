import asyncio
import json
import os
from typing import Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlmodel import SQLModel
from app.main import app
from app.core.config import settings
from app.db.juno_db import async_engine, JunoDB
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
  loop = asyncio.get_event_loop_policy().new_event_loop()
  yield loop
  loop.close()


@pytest_asyncio.fixture
async def async_client():
  async with AsyncClient(
    app = app,
    base_url=f"http://localhost:8080/api/v1"
  ) as client:
    yield client

@pytest_asyncio.fixture
async def async_session() -> AsyncSession:
  db = JunoDB()
  print(settings.db_connection)
  await db.create_tables()
  yield db
