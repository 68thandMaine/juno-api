from fastapi import APIRouter, Depends
from typing import List, Any
from app.models.all import Bill
from app.api import deps
from sqlalchemy.orm import Session
from app import crud

router = APIRouter(prefix="/bills")


@router.get("/", operation_id="get_bills")  # response_model=List[Bill]
async def get_bills(db: Session = Depends(deps.get_db)) -> Any:
    bills = await crud.bill.get_multiple(db)
    return bills
