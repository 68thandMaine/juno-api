from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.juno_db import get_session
from app.models.bill import Bill
from app.services.crud import CRUDService


async def get_bill_crud(session: AsyncSession = Depends(get_session)):
    return CRUDService(session=session, model=Bill)
