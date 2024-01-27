from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel

from app.models.camel_case import CamelCaseModel


class IdBase(CamelCaseModel, SQLModel):
    id: UUID | None = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
    )


@dataclass
class BillBase(SQLModel):
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
    pass


class BillCreate(BillBase):
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
    recurrence_interval: str
    bill_id: Optional[UUID] = Field(default=None, foreign_key="bill.id")


class Category(IdBase, table=True):
    name: str
