from datetime import datetime

from sqlmodel import SQLModel, select

from app.models import Bill, RecurringBill
from app.services.recurring_bill_service import RecurringBillService


class RecurringBillController:
    def __init__(self):
        self.recurring_bill_service = RecurringBillService
        self.current_month = datetime.now().strftime("%B")

    async def get_current_months_bills(self) -> list[Bill]:
        """Method used to get the bills for the current month"""
        result = await self.recurring_bill_service.get_by_recurrence_interval("MONTH")
        return result
