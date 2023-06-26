from sqlmodel import Field, SQLModel
import sqlalchemy
from datetime import date
from typing import Optional
from app.models.camel_case import CamelCaseModel


metadata = sqlalchemy.MetaData()


class Bill(CamelCaseModel, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    amount: int
    due_date: date
    frequency: str
    payment_method: Optional[int] = Field(default=None, foreign_key=True)
    recurring: Optional[bool]
    category: Optional[str]
    status: Optional[str]
    notes: Optional[str]
    archived: bool = Field(default=False)
    logo: Optional[str]
