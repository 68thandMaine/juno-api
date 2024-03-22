from fastapi import APIRouter, Depends

from app.controllers.payment_controller import PaymentController
from app.core.exceptions.crud import (
    handle_get_entity_exception,
    handle_post_entity_exception,
)
from app.core.lib.exceptions import ControllerException
from app.core.lib.utils.time import convert_str_to_datetime
from app.models import Payment

router = APIRouter(prefix="/payment")


@router.get("/", operation_id="get_payments", response_model=list[Payment])
async def get_payments(controller=Depends(PaymentController)) -> list[Payment]:
    try:
        return await controller.get_payments()
    except ControllerException as e:
        await handle_get_entity_exception(e, "payment")
    except Exception as e:
        await handle_get_entity_exception(e, "payment")


@router.post("/", operation_id="new_payment", response_model=Payment)
async def new_payment(
    payment_data: Payment, controller=Depends(PaymentController)
) -> Payment:
    try:
        if not isinstance(payment_data, Payment):
            payment_data = Payment(**payment_data)
        payment = await controller.make_payment(payment_data)
    except ControllerException as e:
        if "cannot be found" in e.detail:
            e.status_code = 412
        await handle_post_entity_exception(e, "new category")
    except Exception as e:
        await handle_post_entity_exception(e, "new category")

    return payment
