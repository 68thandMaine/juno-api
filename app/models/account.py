from sqlmodel import Field, SQLModel, MetaData
from app.models.camel_case import CamelCaseModel
from uuid import UUID, uuid4


accounts_metadata = MetaData()


class AccountsBase(CamelCaseModel, SQLModel):
    metadata = accounts_metadata


class Account(AccountsBase, table=True):
    id: UUID | None = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
    )
    archived: bool = Field(default=False)
    name: str
    type: str
    value: int = Field(default=0)
