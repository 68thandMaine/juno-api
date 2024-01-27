from app.models import Bill, RecurringBill
from app.services.crud import CRUDService


async def get_bill_crud():
    return CRUDService(model=Bill)


async def get_recurring_bill_crud():
    return CRUDService(model=RecurringBill)
