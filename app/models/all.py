from datetime import date
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel
from app.models.camel_case import CamelCaseModel
from decimal import Decimal


class BillBase(CamelCaseModel, SQLModel):
    name: str
    amount: Decimal
    due_date: str
    frequency: str
    recurring: Optional[bool]
    category: Optional[str]
    status: Optional[int]
    notes: Optional[str]
    # payment_method: UUID = Field(default=None, foreign_key="account.id")
    archived: Optional[bool] = Field(default=False)
    logo: Optional[str]


class Bill(BillBase, table=True):
    id: UUID | None = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
    )
