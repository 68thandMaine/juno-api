from uuid import UUID

from app.core.lib.constants import PAYMENT_ERROR_BILL_ID_NOT_FOUND
from app.core.lib.exceptions import ControllerException, NoResultFound, ServiceException
from app.models import Bill, Payment
from app.services.crud import CRUDService


class PaymentController:
    """
    Controller for managing api behaviors related to payments
    """

    def __init__(self):
        self.payment_service = CRUDService(Payment)
        self.bill_service = CRUDService(Bill)

    async def _verify_bill_exists(self, bill_id: UUID) -> bool:
        """Verify if a bill with the given ID exists in the database

        Args:
            bill_id (_type_): The ID of the bill to check.

        Raises:
            NoResultFound: _description_

        Returns:
            bool: True if the bill exists, False otherwise
        """
        found = await self.bill_service.get_one(bill_id)
        if not found:
            raise NoResultFound
        return True

    async def make_payment(self, data: Payment) -> Payment:
        """Used to make payments against a bill"""
        try:
            bill_exists = await self._verify_bill_exists(data.bill_id)
            if bill_exists:
                return await self.payment_service.create(data)
        except NoResultFound as e:
            raise ControllerException(
                status_code=412,
                detail=PAYMENT_ERROR_BILL_ID_NOT_FOUND,
            ) from e
        except ServiceException as e:
            raise ControllerException(
                f"There was an issue with the payment service when making a payment: {e}"
            ) from e
        except Exception as e:
            raise ControllerException(detail=e) from e

    async def get_payments(self) -> list[Payment]:
        """Returns a list of payments"""
        try:
            results = await self.payment_service.get()
        except ServiceException as e:
            raise ControllerException(
                f"There was an issue with the payment service when getting a payment: {e}"
            ) from e
        except Exception as e:
            raise ControllerException(e) from e
        return results
