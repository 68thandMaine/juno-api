from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlmodel import Field

from app.models.common import CamelCaseModel, IdBase


@dataclass
class Payment(IdBase, table=True):
    """
    Represents the payment on a Bill.
    """

    amount: Decimal
    payment_date: datetime
    bill_id: UUID = Field(default=None, foreign_key="bill.id")


@dataclass
class RecurringBill(IdBase, table=True):
    """
    Represents the recurringBill table.
    """

    recurrence_interval: str
    bill_id: Optional[UUID] = Field(default=None, foreign_key="bill.id")


class Category(IdBase, table=True):
    """
    Category represents a group a bill could be classified under.
    """

    name: str


class CategoryInput(CamelCaseModel):
    id: str
    name: str
