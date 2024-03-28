from fastapi import APIRouter, Depends

from app.controllers.bill_controller import BillController
from app.core.exceptions.crud import (
    handle_get_entity_exception,
    handle_update_entity_exception,
)
from app.core.lib.exceptions import ControllerException
from app.models import Bill, BillCreate, BillUpdate

router = APIRouter(prefix="/bills")


@router.get(
    "/",
    operation_id="get_bills",
    response_model=list[Bill],
    summary="Get a list of bills",
    description="Retrieve a list of bills from the database.",
)
async def get_bills(controller=Depends(BillController)) -> list[Bill]:
    try:
        return await controller.get_bills()
    except ControllerException as e:
        await handle_get_entity_exception(e, "bills")


@router.post(
    "/",
    operation_id="add_bill",
    response_model=Bill,
    summary="Add a new bill",
    description="Create a new bill record in the system.",
)
async def add_bill(bill: BillCreate, controller=Depends(BillController)) -> Bill:
    try:
        print(bill.due_date)
        return await controller.add_bill(bill)
    except ValueError as e:
        raise ControllerException(status_code=500, detail=e)
    except ControllerException as e:
        raise ControllerException(status_code=500, detail=e.detail) from e


@router.put("/update/{bill_id}", operation_id="update_bill", response_model=Bill)
async def update_bill(bill: BillUpdate, controller=Depends(BillController)) -> Bill:
    try:
        return await controller.update_bill(bill)
    except ControllerException as e:
        await handle_update_entity_exception(e, "bill")
    except ValueError as e:
        await handle_update_entity_exception(e, "bill")
