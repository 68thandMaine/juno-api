from sqlalchemy.orm.exc import NoResultFound

from app.lib.constants import PAYMENT_ERROR_BILL_ID_NOT_FOUND
from app.lib.exceptions import ControllerException, ServiceException
from app.models import Bill, Payment
from app.services.crud import CRUDService


class PaymentController:
    """
    Controller for managing api behaviors related to payments
    """

    def __init__(self):
        self.payment_service = CRUDService(Payment)
        self.bill_service = CRUDService(Bill)

    async def _verify_bill_exists(self, bill_id) -> bool:
        found = await self.bill_service.get_one(bill_id)
        if not found:
            raise NoResultFound
        return True

    async def make_payment(self, data: Payment) -> Payment:
        """used to make payments against a bill"""
        try:
            bill_exists = await self._verify_bill_exists(data.bill_id)
        except NoResultFound as e:
            raise ControllerException(
                detail=PAYMENT_ERROR_BILL_ID_NOT_FOUND,
            ) from e
        except ServiceException as e:
            raise ControllerException(
                f"There was an issue with the payment service when making a payment: \n{e}"
            ) from e
        except Exception as e:
            raise ControllerException(detail=e) from e

        if bill_exists:
            self.payment_service.create(data)
            return data

    async def get_payments(self) -> list[Payment]:
        """Returns a list of payments"""
        try:
            results = await self.payment_service.get()
        except ServiceException as e:
            raise ControllerException(
                f"There was an issue with the payment service when getting a payment: \n{e}"
            ) from e
        except Exception as e:
            raise ControllerException(e) from e
        return results
