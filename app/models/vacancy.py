# from typing import TYPE_CHECKING, Optional
import enum
from datetime import datetime
from pydantic import model_validator
from sqlalchemy import DateTime, TEXT
from sqlmodel import SQLModel, Field, Column, TIMESTAMP
from .utils import get_datetime_utc, generate_slug_from_name

# if TYPE_CHECKING:
#     from .army_unit import ArmyUnit


class VacancyServiceType(str, enum.Enum):
    COMBAT = "combat"
    REAR = "rear"


# Shared properties
class VacancyBase(SQLModel):
    name: str = Field(min_length=1, max_length=255, index=True)
    slug: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    description: str | None = Field(
        default=None, max_length=1500, sa_column=Column(TEXT)
    )
    responsibilities: str | None = Field(
        default=None, max_length=1500, sa_column=Column(TEXT)
    )
    requirements: str | None = Field(
        default=None, max_length=1500, sa_column=Column(TEXT)
    )
    conditions: str | None = Field(
        default=None, max_length=1500, sa_column=Column(TEXT)
    )
    service_type: VacancyServiceType = Field(default=VacancyServiceType.COMBAT)
    army_unit_id: int = Field(
        foreign_key="army_units.id", nullable=False, ondelete="CASCADE", index=True
    )
    rank_group_id: int | None = Field(
        default=None, foreign_key="rank_groups.id", ondelete="SET NULL", index=True
    )


class VacancyCreate(VacancyBase):
    @model_validator(mode="before")
    @classmethod
    def generate_slug(cls, data):
        return generate_slug_from_name(data)


class VacancyUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    slug: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1500)
    responsibilities: str | None = Field(default=None, max_length=1500)
    requirements: str | None = Field(default=None, max_length=1500)
    conditions: str | None = Field(default=None, max_length=1500)
    service_type: VacancyServiceType | None = Field(default=None)
    army_unit_id: int | None = Field(default=None)
    rank_group_id: int | None = Field(default=None)

    @model_validator(mode="before")
    @classmethod
    def generate_slug(cls, data):
        return generate_slug_from_name(data)


# Database model
class Vacancy(VacancyBase, table=True):
    __tablename__ = "vacancies"  # type: ignore
    id: int | None = Field(default=None, primary_key=True)
    slug: str = Field(  # type: ignore
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
    # army_unit: Optional["ArmyUnit"] = Relationship(back_populates="vacancies")
