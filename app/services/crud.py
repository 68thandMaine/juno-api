from typing import List, Type
from uuid import UUID

from sqlmodel import SQLModel, select

from app.db.juno_db import get_session
from app.lib.constants import CANNOT_UPDATE
from app.lib.exceptions import ServiceException
from app.lib.utils.time import convert_str_to_datetime


class CRUDService:
    """
    CRUDService is the base code used to perform operations and queries against the database.
    """

    def __init__(self, model: Type[SQLModel]):
        self._session = get_session
        self.model = model

    async def _get_by_model_id(self, session, model_id):
        statement = select(self.model).where(self.model.id == model_id)
        return await session.scalar(statement)

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
                db_data = await self._get_by_model_id(session, model_id)
                if not db_data:
                    raise ServiceException(f"{CANNOT_UPDATE} {model_id}")
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
                return await self._get_by_model_id(session, model_id)
        except Exception as e:
            raise ServiceException(e) from e

    async def delete(self, model_id: UUID):
        """Used to delete a resource from a database

        Args:
            model_id (UUID): the id for the entity being removed from the database
        """
        try:
            async for session in self._session():
                result = await self._get_by_model_id(session, model_id)
                await session.delete(result)
                return True
        except Exception as e:
            raise ServiceException(e) from e
