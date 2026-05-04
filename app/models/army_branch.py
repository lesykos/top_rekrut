from typing import TYPE_CHECKING
from pydantic import model_validator
from sqlmodel import Field, SQLModel, Relationship
from .utils import generate_slug_from_name

if TYPE_CHECKING:
    from .army_unit import ArmyUnit


# Shared properties
class ArmyBranchBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    slug: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        # regex=r"^[a-z0-9-]+$",
    )
    position: int = Field(default=30, ge=1, le=30)


class ArmyBranchCreate(ArmyBranchBase):
    @model_validator(mode="before")
    @classmethod
    def generate_slug(cls, data):
        return generate_slug_from_name(data)


class ArmyBranchUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    slug: str | None = Field(default=None, min_length=1, max_length=255)
    position: int | None = Field(default=None, ge=1, le=30)


# Database model
class ArmyBranch(ArmyBranchBase, table=True):
    __tablename__ = "army_branches"  # type: ignore
    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(  # type: ignore
        index=True,
        unique=True,
        nullable=False,
    )
    army_units: list["ArmyUnit"] = Relationship(back_populates="army_branch")


# Properties to return via public API
class ArmyBranchPublic(SQLModel):
    name: str
    slug: str
    position: int


class ArmyBranchesPublic(SQLModel):
    data: list[ArmyBranchPublic]
