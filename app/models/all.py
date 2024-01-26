from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from app.models.camel_case import CamelCaseModel


class IdBase(CamelCaseModel, SQLModel):
    id: UUID | None = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
    )


class Bill(IdBase, table=True):
    name: str
    amount: int
    due_date: datetime
    category: Optional[UUID] = Field(default=None, foreign_key="category.id")
    status: Optional[int]
    # notes: Optional[str]
    # payment_method: UUID = Field(default=None, foreign_key="account.id")
    # archived: Optional[bool] = Field(default=False)
    # logo: Optional[str]


class Payment(IdBase, table=True):
    """
    Represents the payment on a Bill.
    """

    amount: Decimal
    payment_date: datetime
    bill_id: UUID = Field(default=None, foreign_key="bill.id")


class RecurringBill(IdBase, table=True):
    bill_id: UUID = Field(default=None, foreign_key="bill.id")
    recurrence_interval: datetime


class Category(IdBase, table=True):
    name: str


class NewBill(SQLModel):
    name: str
    amount: int
    due_date: str
    category: Optional[str]
    status: Optional[int]
    # recurring: bool
    # recurrence_interval: str
