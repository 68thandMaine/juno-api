from sqlmodel import Field, SQLModel, MetaData
from datetime import date
from typing import Optional
from app.models.camel_case import CamelCaseModel
from uuid import UUID, uuid4

bills_metadata = MetaData()


class Bill(CamelCaseModel, SQLModel, table=True):
    metadata = bills_metadata
    id: UUID | None = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
    )
    name: str
    amount: int
    due_date: date
    frequency: str
    payment_method: Optional[int] = Field(default=None, foreign_key=("account.id"))
    recurring: Optional[bool]
    category: Optional[str]
    status: Optional[str]
    notes: Optional[str]
    archived: bool = Field(default=False)
    logo: Optional[str]
