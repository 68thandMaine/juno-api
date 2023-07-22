from sqlmodel import Field, SQLModel
from datetime import date
from typing import Optional
from app.models.camel_case import CamelCaseModel
from uuid import UUID, uuid4


class Bill(CamelCaseModel, SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    amount: int
    due_date: date
    frequency: str
    # payment_method: Optional[UUID] = Field(default=None, foreign_key="account.id")
    recurring: Optional[bool] = None
    category: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    archived: bool = Field(default=False)
    logo: Optional[str] = None


class BillCreate(CamelCaseModel):
    name: str
    amount: int
    due_date: date
    frequency: str
    recurring: Optional[bool] = None
    category: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
