from uuid import UUID

from sqlalchemy.exc import IntegrityError

from app.lib.exceptions import ControllerException, ServiceException
from app.lib.utils.time import convert_str_to_datetime
from app.models import Bill, BillCreate, BillUpdate, Category, RecurringBill
from app.services.crud import CRUDService


class BillController:
    """
    Controller for handling the various behaviors needed for interacting
    with Bills
    """

    def __init__(
        self,
    ):
        self.bill_service = CRUDService(Bill)
        self.category_service = CRUDService(Category)
        self.recurring_bill_service = CRUDService(RecurringBill)

    async def _add_recurring_bill(self, bill, recurrence_interval):
        try:
            await self.recurring_bill_service.create(
                RecurringBill(bill_id=bill.id, recurrence_interval=recurrence_interval)
            )
        except ServiceException as e:
            raise ControllerException(
                detail=f"There was an error creating recurring bill with the bill service: {str(e)}"
            ) from e
        except Exception as e:
            raise ControllerException(
                f"There was an error adding a recurring bill: \n {e}"
            ) from e

    def _create_bill(self, data: BillCreate) -> Bill:
        try:
            if isinstance(data, dict):
                data = BillCreate(**data)

            return Bill(
                name=data.name,
                amount=data.amount,
                due_date=convert_str_to_datetime(data.due_date),
                category=data.category,
                paid=data.paid,
                auto_pay=data.auto_pay,
            )
        except ValueError as e:
            raise ControllerException(
                detail=f"There was an error with a value when creating a new bill: {e}"
            ) from e
        except Exception as e:
            raise ControllerException(detail=e) from e

    async def add_bill(self, new_bill: BillCreate) -> Bill:
        """
        Controls the flow fo adding a new bill to the database.

        Args:
            new_bill (BillCreate): a representation of a bill that is received by an api.

        Raises:
            ValueError: _description_
            ControllerException: _description_

        Returns:
            Bill: Bill object that was added to the database.
        """
        try:
            category = getattr(new_bill, "category", None)
            if category and not await self.category_service.get_one(category):
                raise ValueError("Category does not exist")
            bill = self._create_bill(new_bill)

            await self.bill_service.create(bill)
            recurring = getattr(new_bill, "recurring", "")

            if recurring and getattr(bill, "id"):
                await self._add_recurring_bill(
                    bill, getattr(new_bill, "recurrence_interval")
                )

        except (ValueError, IntegrityError, ServiceException) as e:
            msg = e
            if isinstance(e, IntegrityError):
                msg = str(e.orig)

            raise ControllerException(
                f" Error adding bill to database ==> {msg}"
            ) from e

        return bill

    async def get_bills(self) -> list[Bill]:
        """
        Returns all of the bills from the database
        """
        try:
            results = await self.bill_service.get()
        except Exception as e:
            raise ControllerException(e) from e
        return results

    async def get_one_bill(self, bill_id: UUID) -> Bill:
        """
        Returns one bill from the database
        """
        try:
            found_bill = await self.bill_service.get_one(bill_id)
        except Exception as e:
            raise ControllerException(
                f"There has been an unexpected issue getting a bill: {e}"
            ) from e
        return found_bill

    async def update_bill(self, bill: BillUpdate) -> Bill:
        """
        Updates a bill

        Accepts a Bill as a parameter. The Bill should contain the updated
        data

        Can be used to delete/archive bills
        """
        bill = Bill(**bill.model_dump())

        db_bill = await self.bill_service.get_one(bill.id)

        if not db_bill:
            raise ValueError(f"No bill with id {bill.id} was found")
        for key in db_bill.model_dump().keys():
            update_value = getattr(bill, key)
            setattr(db_bill, key, update_value)

        try:
            updated_bill = await self.bill_service.put(db_bill.id, db_bill)
        except Exception as e:
            raise ControllerException(
                detail=f"There has been an error updating a bill: \n {e}"
            ) from e

        return updated_bill
