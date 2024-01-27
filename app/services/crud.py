from fastapi import Depends
from typing import Type, List
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel, select
from app.db.juno_db import get_session


class CRUDService:
    def __init__(
        self, model: Type[SQLModel], session: AsyncSession = Depends(get_session)
    ):
        self.session = session
        self.model = model

    async def get(self) -> List[SQLModel]:
        async for row in get_session():
            results = await row.scalars(select(self.model))
        if not results:
            return []
        return results.all()

    async def create(self, data):
        pass
