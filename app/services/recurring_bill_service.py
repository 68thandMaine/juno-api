from app.models import RecurringBill
from app.services.crud import CRUDService


class RecurringBillService(CRUDService):
    """
    Used to return recurring bills.

    Args:
        CRUDService (RecurringBill): Creates a db connection that uses the RecurringBill class
        to create the connection.
    """

    def __init__(self):
        super().__init__(RecurringBill)

    def get_by_recurrence_interval(self):
        # statement = (
        #     select(self.model, Bill)
        #     .join(Bill)
        #     .on(recurrence_interval=BillingFrequency.MONTHLY)
        # )
        return []
