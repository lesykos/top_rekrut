from datetime import datetime
from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel
from .utils import get_datetime_utc


# Shared properties
class ItemBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    desc: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    name: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore[assignment]


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: int
    created_at: datetime | None = None


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Database model, database table inferred from class name (singular name!)
# table=True tells SQLModel that this is a table model,
# it should represent a table in the SQL database.
class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    # could be an datetime or None. Default value by Field() func
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
