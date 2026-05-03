from typing import Sequence
from sqlmodel import Session
from app.core.exceptions import NotFoundError
from app.api.utils import get_offset_limit_from_range
from app.models.army_unit import (
    ArmyUnit,
    ArmyUnitCreate,
    ArmyUnitUpdate,
    # ArmyUnitPublic,
    # ArmyUnitsPublic,
)
from app.repositories import ArmyUnitRepository
from .base import BaseService


class ArmyUnitService(BaseService[ArmyUnit]):
    """Service for ArmyUnit business logic."""

    def __init__(self, session: Session):
        super().__init__(session)
        self.repository = ArmyUnitRepository(session)

    def count_army_units(self, filter_: dict[str, str] | None = None) -> int:
        """Count ArmyUnits with optional filters."""
        return self.repository.count_all(filter_)

    def get_army_unit(self, army_unit_id: int) -> ArmyUnit:
        """Get ArmyUnit by ID"""
        army_unit = self.repository.get_by_id(army_unit_id)
        if army_unit is None:
            raise NotFoundError(f"Army unit {army_unit_id} not found")
        return army_unit

    def get_army_unit_by_slug(self, army_unit_slug: str) -> ArmyUnit:
        """Get ArmyUnit by slug"""
        army_unit = self.repository.get_by_slug(army_unit_slug)
        if army_unit is None:
            raise NotFoundError(f"Army unit {army_unit_slug} not found")
        return army_unit

    def get_army_units(
        self,
        sort: list[str] | None = None,
        range_: list[int] | None = None,
        filter_: dict[str, str] | None = None,
    ) -> Sequence[ArmyUnit]:
        """Get a list of ArmyUnits"""
        offset, limit = get_offset_limit_from_range(range_)
        return self.repository.get_all(sort, filter_, offset, limit)

    # def get_army_units_public(self) -> ArmyUnitsPublic:
    #     """Get a list of public ArmyUnits"""
    #     army_units = self.repository.get_all()
    #     army_units_public = [
    #         ArmyUnitPublic.model_validate(army_unit) for army_unit in army_units
    #     ]
    #     return ArmyUnitsPublic(data=army_units_public, count=len(army_units_public))

    def create_army_unit(self, army_unit_data: ArmyUnitCreate) -> ArmyUnit:
        """Create new ArmyUnit"""
        return self.repository.create_from_data(army_unit_data)

    def update_army_unit(
        self, army_unit_id: int, army_unit_data: ArmyUnitUpdate
    ) -> ArmyUnit:
        """Update existing ArmyUnit (by ID)"""
        existing_army_unit = self.get_army_unit(army_unit_id)
        return self.repository.update_from_data(existing_army_unit, army_unit_data)

    def update_army_unit_by_slug(
        self, army_unit_slug: str, army_unit_data: ArmyUnitUpdate
    ) -> ArmyUnit:
        """Update existing ArmyUnit"""
        existing_army_unit = self.get_army_unit_by_slug(army_unit_slug)
        return self.repository.update_from_data(existing_army_unit, army_unit_data)

    def delete_army_unit(self, army_unit_id: int) -> None:
        """Delete existing ArmyUnit"""
        existing_army_unit = self.get_army_unit(army_unit_id)
        self.repository.delete(existing_army_unit)
