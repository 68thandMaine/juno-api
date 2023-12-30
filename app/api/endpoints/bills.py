from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.all import Bill
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.db.juno_db import JunoDB, get_session

router = APIRouter(prefix="/bills")


@router.get("/", operation_id="get_bills", response_model=List[Bill])
async def get_bills(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Bill))
    bills = result.scalars().all()
    return bills


@router.post("/", operation_id="add_bill", response_model=Bill)
async def add_bill(bill: Bill, session: AsyncSession = Depends(get_session)):
    
    new_bill = Bill(
        name=bill.name,
        amount=bill.amount,
        due_date=bill.due_date,
        category=bill.category,
        status=bill.status,
        
    )
    session.add(new_bill)
    await session.commit()
    await session.refresh(new_bill)
    return new_bill


@router.put("/update/{id}", operation_id="update_bill")
async def update_bill(bill: Bill, session: AsyncSession = Depends(get_session)):
    new_bill = Bill(**bill)
    statement = select(Bill).where(Bill.id == bill.id)
    results = session.exec(statement)
    bill = results.one()
    bill = new_bill
    session.add(bill)
    session.commit()
    session.refresh(bill)
