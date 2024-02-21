from fastapi import APIRouter, Depends, HTTPException

from app.controllers.payment_controller import PaymentController
from app.lib.exceptions import ControllerException
from app.lib.utils.time import convert_str_to_datetime
from app.models import Payment

router = APIRouter(prefix="/payment")


async def handle_get_payments_exception(e: Exception):
    raise HTTPException(
        status_code=500,
        detail=f"Error getting payments using payment controller: {str(e)}",
    ) from e


async def handle_new_payment_exception(e: Exception):
    raise HTTPException(
        status_code=e.status_code, detail=f"Failed to create payment: {str(e)}"
    ) from e


@router.get("/", operation_id="get_payments", response_model=list[Payment])
async def get_payments(controller=Depends(PaymentController)) -> list[Payment]:
    try:
        return await controller.get_payments()
    except ControllerException as e:
        await handle_get_payments_exception(e)
    except Exception as e:
        await handle_get_payments_exception(e)


@router.post("/", operation_id="new_payment", response_model=Payment)
async def new_payment(
    payment_data: Payment, controller=Depends(PaymentController)
) -> Payment:
    try:
        if not isinstance(payment_data, Payment):
            payment_data = Payment(**payment_data)
        payment_data.payment_date = convert_str_to_datetime(payment_data.payment_date)
        payment = await controller.make_payment(payment_data)
    except ControllerException as e:
        if "cannot be found" in e.detail:
            e.status_code = 412
        await handle_new_payment_exception(e)
    except Exception as e:
        await handle_new_payment_exception(e)

    return payment
