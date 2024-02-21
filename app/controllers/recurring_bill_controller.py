from datetime import datetime

from app.lib.exceptions import ControllerException, ServiceException
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
            raise ControllerException(
                f"There was an issue with the recurring bill service when getting a this months bills: {e}"
            ) from e
        except Exception as e:
            raise ControllerException(e) from e
