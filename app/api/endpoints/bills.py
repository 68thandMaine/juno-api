from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.juno_db import get_session
from app.models.all import Bill, NewBill


router = APIRouter(prefix="/bills")


@router.get("/", operation_id="get_bills")
async def get_bills(session: AsyncSession = Depends(get_session)) -> List[Bill]:
    result = await session.execute(select(Bill))
    bills = result.scalars().all()
    if not bills:
        return []
    return bills


@router.post("/", operation_id="add_bill", response_model=Bill)
async def add_bill(bill: NewBill, session: AsyncSession = Depends(get_session)):
    try:
        new_bill = Bill(
            name=bill.name,
            amount=bill.amount,
            due_date=datetime.fromisoformat(bill.due_date),
            category=bill.category,
            status=bill.status,
        )
        session.add(new_bill)
        await session.commit()
        await session.refresh(new_bill)

        return new_bill
    except Exception as e:
        raise AttributeError(e)


@router.put("/update/{id}", operation_id="update_bill")
async def update_bill(bill: Bill, session: AsyncSession = Depends(get_session)):
    statement = select(Bill).where(Bill.id == bill.id)
    db_result = await session.execute(statement)
    bill_to_update = db_result.scalar_one()

    for k, v in bill.model_dump().items():
        if k == "due_date":
            v = datetime.fromisoformat(v)
        setattr(bill_to_update, k, v)

    session.add(bill_to_update)
    await session.commit()
    await session.refresh(bill_to_update)

    return bill_to_update
