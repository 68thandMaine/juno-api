from fastapi import APIRouter, Depends
from typing import List
from app.models.all import Bill, BillCreate
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.db.db import get_session, init_db

router = APIRouter(prefix="/bills")


# Endpoint to get all bills
@router.get("/", response_model=List[Bill], tags=["Bills"], operation_id="getBills")
async def get_bills(session: AsyncSession = Depends(get_session)):
    async with session.begin():
        query = select(Bill)
        result = await session.exec(query)
        return result.fetchall()


# Endpoint to get a single bill by ID
@router.get("/{bill_id}", response_model=Bill, tags=["Bills"], operation_id="getBill")
async def get_bill(bill_id: int, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        result = await session.get(Bill, bill_id)
        return result


# Endpoint to add a new bill
@router.post("/", response_model=Bill, tags=["Bills"], operation_id="createNewBill")
async def add_bill(bill: BillCreate, session: AsyncSession = Depends(get_session)):
    new_bill = Bill(**bill.dict())
    session.add(new_bill)
    await session.commit()
    await session.refresh(new_bill)
    return new_bill
