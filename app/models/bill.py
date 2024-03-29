from dataclasses import dataclass
from datetime import datetime
from enum import Enum
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
    paid: Optional[bool] = False
    category: Optional[UUID] = Field(default=None, foreign_key="category.id")
    auto_pay: bool
    # notes: Optional[str]
    # payment_method: UUID = Field(default=None, foreign_key="account.id")
    # archived: Optional[bool] = Field(default=False)
    # logo: Optional[str]


class BillCreate(BillBase):
    """
    Bill sent from the client.

    Notable differences between this and Billbase is that
    the due_date is a str instead of a python date.
    """

    due_date: str  # type: ignore
    recurring: bool
    recurrence_interval: Optional[str]


class BillUpdate(BillBase):
    """
    Class used to update Bill entities.

    It is used when receiving data in json format,
    so the id and due_date properties need to be in str form as opposed to UUID and
    datetime.
    """

    id: str  # type:ignore
    due_date: str  # type: ignore


@dataclass
class Bill(IdBase, BillBase, table=True):
    """
    Bill table
    """


class BillingFrequency(Enum):
    """Represents the frequency of which a bill should be charged"""

    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    SEMIANNUAL = "semiannual"
    ANNUAL = "annual"
