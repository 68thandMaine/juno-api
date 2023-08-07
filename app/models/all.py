from datetime import date
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel
from app.models.camel_case import CamelCaseModel
from decimal import Decimal


class BaseTableModel(SQLModel, CamelCaseModel, table=True):
    id: int = Field(primary_key=True, index=True, unique=True, default=1)


class Account(BaseTableModel):
    archived: bool = Field(default=False)
    name: str
    type: str
    value: Decimal = 0.00


class BillCreate(CamelCaseModel):
    name: str
    amount: Decimal
    due_date: date
    frequency: str
    recurring: Optional[bool]
    category: Optional[str]
    status: Optional[str]
    notes: Optional[str]


class Bill(BaseTableModel, BillCreate):
    payment_method: Optional[int] = Field(default=None, foreign_key="account.id")
    archived: bool = Field(default=False)
    logo: Optional[str] = None
