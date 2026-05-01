from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlalchemy import DateTime, String
from pydantic import HttpUrl, model_validator, field_validator
from sqlmodel import Field, SQLModel, Relationship, TIMESTAMP
from slugify import slugify
from .utils import get_datetime_utc

if TYPE_CHECKING:
    from .army_branch import ArmyBranch


# Shared properties
class ArmyUnitBase(SQLModel):
    name: str = Field(min_length=1, max_length=255, index=True)
    slug: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        # regex=r"^[a-z0-9-]+$",
    )
    description: str | None = Field(default=None, min_length=1, max_length=255)
    website: HttpUrl | None = Field(default=None, sa_type=String)


class ArmyUnitCreate(ArmyUnitBase):
    army_branch_id: int | None = Field(default=None)

    @model_validator(mode="before")
    @classmethod
    def generate_slug(cls, data):
        # Generate slug from name if it's not provided
        if not data.get("slug") and data.get("name"):
            data["slug"] = slugify(data["name"])
        return data

    @field_validator("website", mode="after")
    @classmethod
    def serialize_url(cls, v):
        return str(v) if v else None


class ArmyUnitUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    slug: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=1, max_length=255)
    website: HttpUrl | None = Field(default=None, sa_type=String)
    army_branch_id: int | None = Field(default=None)

    @field_validator("website", mode="after")
    @classmethod
    def serialize_url(cls, v):
        return str(v) if v else None


# Database model
class ArmyUnit(ArmyUnitBase, table=True):
    __tablename__ = "army_units"  # type: ignore
    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(  # type: ignore
        index=True,
        unique=True,
        nullable=False,
    )
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        nullable=False,
        sa_column_kwargs={
            "onupdate": get_datetime_utc,
        },
        sa_type=TIMESTAMP(timezone=True),  # type: ignore
    )
    army_branch_id: int | None = Field(
        default=None, foreign_key="army_branches.id", ondelete="SET NULL", index=True
    )
    army_branch: Optional["ArmyBranch"] = Relationship(back_populates="army_units")
