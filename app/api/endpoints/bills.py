from fastapi import APIRouter, Depends, HTTPException

from app.controllers.bill_controller import BillController
from app.lib.exceptions import ControllerException
from app.models import Bill, BillCreate, BillUpdate

router = APIRouter(prefix="/bills")


async def handle_get_bills_exception(e: Exception):
    raise HTTPException(
        status_code=500, detail=f"Failed to get bills because \n {str(e)}"
    ) from e


async def handle_add_bill_exception(bill: BillCreate, e: Exception):
    raise HTTPException(
        status_code=500,
        detail=f"Failed to add bill for {bill.name} because \n {str(e)}",
    ) from e


async def handle_update_bill_exception(e: Exception):
    raise HTTPException(
        status_code=500,
        detail=f"Failed to update bill because \n {str(e)}",
    ) from e


@router.get("/", operation_id="get_bills", response_model=list[Bill])
async def get_bills(controller=Depends(BillController)) -> list[Bill]:
    try:
        return await controller.get_bills()
    except ControllerException as e:
        await handle_get_bills_exception(e)


@router.post("/", operation_id="add_bill", response_model=Bill)
async def add_bill(bill: BillCreate, controller=Depends(BillController)) -> Bill:
    try:
        return await controller.add_bill(bill)
    except ControllerException as e:
        raise ControllerException(status_code=500, detail=e.detail) from e


@router.put("/update/{bill_id}", operation_id="update_bill", response_model=Bill)
async def update_bill(bill: BillUpdate, controller=Depends(BillController)) -> Bill:
    try:
        return await controller.update_bill(bill)
    except ControllerException as e:
        await handle_update_bill_exception(e)
    except ValueError as e:
        await handle_update_bill_exception(e)
