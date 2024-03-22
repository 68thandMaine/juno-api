from uuid import UUID

from pydantic_core import ValidationError
from sqlalchemy.exc import IntegrityError

from app.core.exceptions.controller import (
    handle_error_in_service,
    handle_generic_exception,
    handle_value_error_in_service,
)
from app.core.lib.exceptions import ControllerException, ServiceException
from app.core.lib.utils.time import convert_str_to_datetime
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
        """
        Add a recurring bill to the database for the specified bill.

        Args:
            bill: The bill for which the recurring bill is added.
            recurrence_interval (str): The recurrence interval for the recurring bill.

        Raises:
            ControllerException: If there is an error creating or adding the recurring bill.
        """
        try:
            await self.recurring_bill_service.create(
                RecurringBill(bill_id=bill.id, recurrence_interval=recurrence_interval)
            )
        except ServiceException as e:
            handle_error_in_service(e, "add recurring bill")
        except Exception as e:
            handle_generic_exception(e, "add recurring bill")

    async def _create_bill(self, data: BillCreate) -> Bill:
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
            handle_value_error_in_service(e)
        except Exception as e:
            handle_generic_exception(e, "_create_bill")

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

            bill = await self._create_bill(new_bill)
            await self.bill_service.create(bill)

            recurring = getattr(new_bill, "recurring", "")

            if recurring and getattr(bill, "id"):
                await self._add_recurring_bill(
                    bill, getattr(new_bill, "recurrence_interval")
                )

        except (
            ValueError,
            ServiceException,
            ControllerException,
        ) as e:

            if isinstance(e, ValueError):
                await handle_value_error_in_service(e)

            if isinstance(e, ServiceException):
                await handle_value_error_in_service(e)

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
        except ServiceException as e:
            await handle_error_in_service(e, "bill_service.get")
        return found_bill

    async def update_bill(self, bill: Bill) -> Bill:
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
            await handle_generic_exception(e, "update bill")
        return updated_bill
