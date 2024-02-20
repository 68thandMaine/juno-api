from fastapi import APIRouter, Depends, HTTPException
from app.lib.exceptions import ControllerException
from app.controllers.bill_controller import BillController
from app.models import Bill, BillCreate, BillUpdate

router = APIRouter(prefix="/bills")


@router.get("/", operation_id="get_bills", response_model=list[Bill])
async def get_bills(controller=Depends(BillController)) -> list[Bill]:
    try:
        bills = await controller.get_bills()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get bills because \n {str(e)}"
        ) from e
    return bills


@router.post("/", operation_id="add_bill", response_model=Bill)
async def add_bill(bill: BillCreate, controller=Depends(BillController)) -> Bill:
    try:
        bill = await controller.add_bill(bill)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add bill for {bill.name} because \n {str(e)}",
        ) from e
    return bill


@router.put("/update/{bill_id}", operation_id="update_bill", response_model=Bill)
async def update_bill(bill: BillUpdate, controller=Depends(BillController)) -> Bill:
    try:
        updated_bill = await controller.update_bill(bill)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update bill because \n {str(e)}",
        ) from e
    return updated_bill
