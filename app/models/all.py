from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel

from app.models.camel_case import CamelCaseModel


class IdBase(CamelCaseModel, SQLModel):
    """
    Provides the base ID for all models and introduces code to
    swap snake_case and camel case.
    """

    id: UUID | None = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
    )


@dataclass
class BillBase(SQLModel):
    """
    Basic properties of a bill
    """

    name: str
    amount: int
    due_date: datetime
    status: Optional[int]
    category: Optional[UUID] = Field(default=None, foreign_key="category.id")
    # notes: Optional[str]
    # payment_method: UUID = Field(default=None, foreign_key="account.id")
    # archived: Optional[bool] = Field(default=False)
    # logo: Optional[str]


class Bill(BillBase, IdBase, table=True):
    """
    This class represents a table with columns that map to the BillBase.
    """

    pass


class BillCreate(BillBase):
    """
    We expect to see this object when new bills are received in API requests
    """

    recurring: bool
    recurrence_interval: Optional[str]


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
