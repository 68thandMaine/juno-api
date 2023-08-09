from fastapi import APIRouter, Depends
from typing import List
from app.models.all import Bill
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.db.db import get_session, init_db

router = APIRouter(prefix="/bills")


@router.get("/", operation_id="get_bills", response_model=List[Bill])
async def get_bills(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Bill))
    bills = result.scalars().all()
    return bills


@router.post("/", operation_id="add_bill", response_model=Bill)
async def add_bill(bill: Bill, session: AsyncSession = Depends(get_session)):
    new_bill = Bill(
        name=bill.name,
        amount=bill.amount,
        due_date=bill.due_date,
        frequency=bill.frequency,
        recurring=bill.recurring,
        category=bill.category,
        status=bill.status,
        notes=bill.notes,
    )
    session.add(new_bill)
    await session.commit()
    await session.refresh(new_bill)
    return new_bill
