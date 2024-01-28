from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.dependencies import get_bill_crud, get_recurring_bill_crud
from app.lib.utils.time import convert_str_to_datetime
from app.models import Bill, BillCreate, RecurringBill

router = APIRouter(prefix="/bills")


@router.get("/", operation_id="get_bills", response_model=list)
async def get_bills(bill_crud=Depends(get_bill_crud)):
    bills = await bill_crud.get()
    return bills


@router.post("/", operation_id="add_bill", response_model=Bill)
async def add_bill(
    bill: BillCreate,
    bill_crud=Depends(get_bill_crud),
    recurring_bill_crud=Depends(get_recurring_bill_crud),
):
    try:
        new_bill = Bill(
            name=bill.name,
            amount=bill.amount,
            due_date=convert_str_to_datetime(bill.due_date),
            category=bill.category,
            status=bill.status,
        )
        await bill_crud.create(new_bill)

        if bill.recurring and new_bill.id and bill.recurrence_interval:
            recurring_bill = RecurringBill(
                bill_id=new_bill.id,
                recurrence_interval=bill.recurrence_interval,
            )
            recurring_bill_crud.create(recurring_bill)

        return new_bill
    except Exception as e:
        raise AttributeError(e) from e


@router.put("/update/{bill_id}", operation_id="update_bill")
async def update_bill(bill_id: str, bill: Bill, bill_crud=Depends(get_bill_crud)):
    updated_bill = await bill_crud.put(bill_id, bill)
    return updated_bill
