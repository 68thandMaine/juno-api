from typing import List, Type
from uuid import UUID

from sqlmodel import SQLModel, select

from app.db.juno_db import get_session
from app.lib.exceptions import ServiceException
from app.lib.utils.time import convert_str_to_datetime


class CRUDService:
    """
    CRUDService is the base code used to perform operations and queries against the database.
    """

    def __init__(self, model: Type[SQLModel]):
        self._session = get_session
        self.model = model

    async def _add_to_database(self, session, data):
        """
        Code that simplifies adding and updating data in db
        """

        session.add(data)
        await session.commit()
        await session.refresh(data)

    async def get(self) -> List[SQLModel]:
        """
        Gets members of the model
        """
        try:
            async for session in self._session():
                results = await session.scalars(select(self.model))
        except Exception as e:
            raise ServiceException(e) from e
        return results.all() if results else []

    async def create(self, data: Type[SQLModel]):
        """
        Creates a new member of the model and returns the data
        """
        try:
            async for session in self._session():
                await self._add_to_database(session, data)
                return data
        except Exception as e:
            raise ServiceException(e) from e

    async def put(self, model_id: UUID, data: Type[SQLModel]):
        """
        Updates a member of the model being queried
        """
        try:
            async for session in self._session():
                statement = select(self.model).where(self.model.id == model_id)
                db_data = await session.scalar(statement)
                if not db_data:
                    raise ServiceException(
                        f"Cannot update because no data with id {model_id} can be found"
                    )
                for k, v in data.model_dump().items():  # type: ignore
                    if k == "due_date" and isinstance(v, str):
                        v = convert_str_to_datetime(v)
                    setattr(db_data, k, v)

                await self._add_to_database(session, db_data)
        except Exception as e:
            raise ServiceException(e) from e
        return db_data

    async def get_one(self, model_id: UUID):
        """
        Returns one of the model being queried for
        """
        try:
            async for session in self._session():
                statement = select(self.model).where(self.model.id == model_id)
                data = await session.scalar(statement)
                await session.close()
        except Exception as e:
            raise ServiceException(e) from e
        return data

    async def delete(self, model_id: UUID):
        try:
            async for session in self._session():
                statement = select(self.model).where(self.model.id == model_id)
                result = await session.scalar(statement)
                await session.delete(result)
                await session.close()
                return True
        except Exception as e:
            raise ServiceException(e) from e
