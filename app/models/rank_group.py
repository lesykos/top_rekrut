from pydantic import model_validator
from sqlmodel import Field, SQLModel
from .utils import generate_slug_from_name


# Shared properties
class RankGroupBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    slug: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    position: int = Field(default=9, ge=1, le=9)


class RankGroupCreate(RankGroupBase):
    @model_validator(mode="before")
    @classmethod
    def generate_slug(cls, data):
        return generate_slug_from_name(data)


class RankGroupUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    slug: str | None = Field(default=None, min_length=1, max_length=255)
    position: int | None = Field(default=None, ge=1, le=9)


# Database model
class RankGroup(RankGroupBase, table=True):
    __tablename__ = "rank_groups"  # type: ignore
    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(  # type: ignore
        index=True,
        unique=True,
        nullable=False,
    )


# Properties to return via public API
class RankGroupPublic(SQLModel):
    id: int
    name: str
    slug: str
    position: int


class RankGroupsPublic(SQLModel):
    data: list[RankGroupPublic]
