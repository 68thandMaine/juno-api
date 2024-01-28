from fastapi import APIRouter, Depends, HTTPException

from app.controllers.payment_controller import PaymentController
from app.models import Payment

router = APIRouter(prefix="/payment")


@router.get("/", operation_id="get_payments")
async def get_payments(controller=Depends(PaymentController)):
    """
    Return a list of all payments or just a list.
    """
    payments = await controller.get_payments()
    return payments


@router.post("/", operation_id="new_payment")
async def new_payment(payment_data: Payment, controller=Depends(PaymentController)):
    """
    Creates a new payment against a bill.
    """
    try:
        payment = await controller.make_payment(payment_data)
    except Exception as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    return payment
