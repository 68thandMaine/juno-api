from sqlmodel import Field, SQLModel
from datetime import date
from typing import Optional
from app.models.camel_case import CamelCaseModel
from uuid import UUID, uuid4


class BaseTableModel(CamelCaseModel, SQLModel):
    id: int = Field(default=None, primary_key=True, index=True, unique=True)


class Account(BaseTableModel, table=True):
    archived: bool = Field(default=False)
    name: str
    type: str
    value: float = 0.00


class Bill(BaseTableModel, table=True):
    name: str
    amount: float
    due_date: date
    frequency: str
    payment_method: Optional[int] = Field(default=None, foreign_key="account.id")
    recurring: Optional[bool] = None
    category: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    archived: bool = Field(default=False)
    logo: Optional[str] = None


class BillCreate(CamelCaseModel):
    name: str
    amount: float
    due_date: date
    frequency: str
    recurring: Optional[bool] = None
    category: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
