# from typing import Any
from pydantic import model_validator
from sqlmodel import Field, SQLModel
from slugify import slugify


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
        # Generate slug from name if it's not provided
        if not data.get("slug") and data.get("name"):
            data["slug"] = slugify(data["name"])
        return data


class RankGroupUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    slug: str | None = Field(default=None, min_length=1, max_length=255)
    position: int | None = Field(default=None, ge=1, le=9)


# Database model, db table inferred from class name
class RankGroup(RankGroupBase, table=True):
    __tablename__ = "rank_groups"  # type: ignore
    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(  # type: ignore
        index=True,
        unique=True,
        nullable=False,
    )


# Properties to return via API
class RankGroupPublic(RankGroupBase):
    pass


class RankGroupsPublic(SQLModel):
    data: list[RankGroupPublic]
    count: int
