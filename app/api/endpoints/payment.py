from fastapi import APIRouter, Depends, HTTPException

from app.controllers.payment_controller import PaymentController
from app.lib.exceptions import ControllerException, ServiceException
from app.models import Payment

router = APIRouter(prefix="/payment")


@router.get("/", operation_id="get_payments", response_model=list[Payment])
async def get_payments(controller=Depends(PaymentController)) -> list[Payment]:
    """
    Return a list of all payments or just a list.
    """
    try:
        payments = await controller.get_payments()
    except ControllerException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=f"Error getting payments using payment controller: \n {str(e.detail)}",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get payments: {str(e)}"
        ) from e
    return payments


@router.post("/", operation_id="new_payment", response_model=Payment)
async def new_payment(
    payment_data: Payment, controller=Depends(PaymentController)
) -> Payment:
    """
    Creates a new payment against a bill.
    """
    try:
        payment = await controller.make_payment(payment_data)

    except ControllerException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=f"Error creating payment using payment controller: \n {e.detail}",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create payment: {str(e)}"
        ) from e
    return payment
