import asyncio
from typing import AsyncGenerator

import psycopg2
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.db.juno_db import get_session
from app.main import app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://localhost:8000/v1/") as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncGenerator:
    return get_session()


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_database(request):
    connection = psycopg2.connect(
        dbname="juno_db_test",
        user=settings.db_username,
        password=settings.db_password,
        host=settings.db_username,
        port=settings.db_port,
    )

    # Create a cursor
    cursor = connection.cursor()

    # Yield the connection and cursor to the test function
    yield connection, cursor

    # Cleanup: Delete entries from multiple tables
    tables_to_cleanup = ["bill", "category", "payment", "recurringbill"]

    for table in tables_to_cleanup:
        cursor.execute(f"DELETE FROM {table}")

    # Commit the changes and close the cursor and connection
    connection.commit()
    cursor.close()
    connection.close()
