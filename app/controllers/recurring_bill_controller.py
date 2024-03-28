from datetime import datetime

from app.core.exceptions.controller import (
    handle_error_in_service,
    handle_generic_exception,
)
from app.core.lib.exceptions import ServiceException
from app.models import Bill
from app.services.recurring_bill_service import RecurringBillService


class RecurringBillController:
    """
    Class for controlling behavior related to recurring bills
    """

    def __init__(self):
        self.recurring_bill_service = RecurringBillService
        self.current_month = datetime.now().strftime("%B")

    async def get_current_months_bills(self) -> list[Bill]:
        """Method used to get the bills for the current month"""
        try:
            return await self.recurring_bill_service.get_by_recurrence_interval("MONTH")
        except ServiceException as e:
            await handle_error_in_service(
                e, "recurring_bill_service.get_by_recurrence_interval"
            )
        except Exception as e:
            await handle_generic_exception(e, "get_current_months_bills")
