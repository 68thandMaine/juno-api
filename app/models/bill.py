from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Field

from app.models.common import CamelCaseModel, IdBase


class BillBase(CamelCaseModel):
    """
    Base properties for a bill
    """

    name: str
    amount: int
    due_date: datetime
    paid: Optional[int]
    category: Optional[UUID] = Field(default=None, foreign_key="category.id")
    autoPay: bool
    # notes: Optional[str]
    # payment_method: UUID = Field(default=None, foreign_key="account.id")
    # archived: Optional[bool] = Field(default=False)
    # logo: Optional[str]


class BillCreate(BillBase):
    """
    Object sent in API requests that maps that maps to two tables.
    """

    due_date: str  # type: ignore
    recurring: bool
    recurrence_interval: Optional[str]


@dataclass
class Bill(IdBase, BillBase, table=True):
    """
    Bill table
    """
