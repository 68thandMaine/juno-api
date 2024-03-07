from typing import Union
from uuid import UUID

from app.core.exceptions.controller import (
    handle_error_in_service,
    handle_generic_exception,
    handle_not_found_exception,
)
from app.core.lib.constants import PAYMENT_ERROR_BILL_ID_NOT_FOUND
from app.core.lib.exceptions import NoResultFound, ServiceException
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

    async def make_payment(self, data: Payment) -> Union[Payment, None]:
        """Used to make payments against a bill"""
        try:
            bill_exists = await self._verify_bill_exists(data.bill_id)

        except NoResultFound:
            await handle_not_found_exception(PAYMENT_ERROR_BILL_ID_NOT_FOUND)
        except ServiceException as e:
            await handle_error_in_service(e, "payment_service.create")
        except Exception as e:
            await handle_generic_exception(e, "make_payment")
        return await self.payment_service.create(data) if bill_exists else None

    async def get_payments(self) -> list[Payment]:
        """Returns a list of payments"""
        try:
            results = await self.payment_service.get()
        except ServiceException as e:
            await handle_error_in_service(e, "payment_service.get")
        except Exception as e:
            await handle_generic_exception(e, "get_payments")
        return results
