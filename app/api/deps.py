from typing import Generator
from app.db.juno_tables import SessionFactory


async def get_db() -> Generator:
    try:
        db = SessionFactory()
        yield db
    finally:
        await db.close()
