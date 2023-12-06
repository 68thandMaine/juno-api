from fastapi import APIRouter, Depends, HTTPException
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


@router.put("/update/{id}", operation_id="update_bill")
async def update_bill(bill: Bill, session: AsyncSession = Depends(get_session)):
    new_bill = Bill(**bill)
    print(new_bill)
    statement = select(Bill).where(Bill.id == bill.id)
    results = session.exec(statement)
    bill = results.one()
    print("db bill", bill)
    bill = new_bill
    session.add(bill)
    session.commit()
    session.refresh(bill)
    print("updated bill", bill)
