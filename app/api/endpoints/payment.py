from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.exc import NoResultFound
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.juno_db import get_session
from app.lib.constants import PAYMENT_ERROR_BILL_ID_NOT_FOUND
from app.models.all import Bill, Payment

router = APIRouter(prefix="/payment")


@router.get("/", operation_id="get_payments")
async def get_payments(session: AsyncSession = Depends(get_session)):
    """
    Return a list of all payments or just a list.
    """
    result = await session.execute(select(Payment))
    payments = result.scalars().all()
    if not payments:
        return []
    return payments


@router.post("/", operation_id="new_payment")
async def new_payment(
    payment_data: Payment, session: AsyncSession = Depends(get_session)
):
    """
    Creates a new payment against a bill.
    """
    # verify bill exists. If it doesn't then raise 412 error
    # ! Refactor into service
    try:
        result = await session.execute(
            select(Bill).where(Bill.id == payment_data.bill_id)
        )
        bill = result.scalar_one()
    except NoResultFound as e:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=PAYMENT_ERROR_BILL_ID_NOT_FOUND,
        ) from e

    # submit the payment record
    payment = Payment(
        amount=payment_data.amount,
        payment_date=datetime.fromisoformat(str(payment_data.payment_date)),
        bill_id=bill.id,
    )
    session.add(payment)
    await session.commit()
    await session.refresh(payment)

    return payment
