from typing import List, Type
from uuid import UUID

from sqlmodel import SQLModel, select

from app.db.juno_db import get_session
from app.lib.utils.time import convert_str_to_datetime


class CRUDService:
    """
    CRUDService is the base code used to perform operations and queries against the database.
    """

    def __init__(self, model: Type[SQLModel]):
        self.session = get_session()
        self.model = model

    async def _add_to_database(self, session, data):
        """
        Code that simplifies adding and updating data in db
        """
        session.add(data)
        await session.commit()
        await session.refresh(data)
        await session.close()

    async def get(self) -> List[SQLModel]:
        """
        Gets members of the model
        """
        async for session in self.session:
            results = await session.scalars(select(self.model))
            await session.close()
        if not results:
            return []
        return results.all()

    async def create(self, data: Type[SQLModel]):
        """
        Creates a new member of the model
        """
        async for session in self.session:
            await self._add_to_database(session, data)

    async def put(self, model_id: UUID, data: Type[SQLModel]):
        """
        Updates a member of the model being queried
        """
        async for session in self.session:
            statement = select(self.model).where(self.model.id == model_id)
            db_data = await session.scalar(statement)

            for k, v in data.model_dump().items():  # type: ignore
                if k == "due_date":
                    v = convert_str_to_datetime(v)
                setattr(db_data, k, v)

            await self._add_to_database(session, db_data)

        return db_data

    async def get_one(self, model_id: UUID):
        """
        Returns one of the model being queried for
        """
        async for session in self.session:
            statement = select(self.model).where(self.model.id == model_id)
            data = await session.scalar(statement)
            await session.close()
            return data
