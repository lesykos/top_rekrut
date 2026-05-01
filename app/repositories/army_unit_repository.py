from typing import Sequence
from sqlmodel import select, col
from sqlalchemy.exc import IntegrityError
from app.core.exceptions import ValidationError, ConflictError
from app.models.army_unit import ArmyUnit, ArmyUnitCreate, ArmyUnitUpdate
from .base import BaseRepository

# from sqlalchemy.orm import joinedload


class ArmyUnitRepository(BaseRepository[ArmyUnit]):

    def get_model_class(self) -> type[ArmyUnit]:
        return ArmyUnit

    def get_all(self) -> Sequence[ArmyUnit]:
        """Get all ArmyUnits ordered by ID."""
        #
        return self.session.exec(
            select(ArmyUnit).order_by(col(ArmyUnit.id).desc())
        ).all()

    def get_by_slug(self, slug: str) -> ArmyUnit | None:
        """Get ArmyUnit by slug."""
        res = self.session.exec(
            select(ArmyUnit).where(ArmyUnit.slug == slug)
            # .options(joinedload(ArmyUnit.army_branch))  # type: ignore
        ).first()
        return res

    def create_from_data(self, army_unit_data: ArmyUnitCreate) -> ArmyUnit:
        """Create ArmyUnit from ArmyUnitCreate data"""
        try:
            army_unit = ArmyUnit(**army_unit_data.model_dump())
            return self.create(army_unit)
        except IntegrityError as e:
            self.session.rollback()
            if "ix_army_units_slug" in str(e.orig):
                raise ValidationError("Key (slug) already exists.") from None

            raise ConflictError("Database integrity error") from e

    def update_from_data(
        self, army_unit: ArmyUnit, army_unit_data: ArmyUnitUpdate
    ) -> ArmyUnit:
        """Update ArmyUnit from ArmyUnitUpdate data"""
        try:
            update_data = army_unit_data.model_dump(
                exclude_unset=True, exclude_none=True
            )
            army_unit.sqlmodel_update(update_data)
            return self.update(army_unit)
        except IntegrityError as e:
            self.session.rollback()
            if "ix_army_units_slug" in str(e.orig):
                raise ValidationError("Key (slug) already exists.") from None

            raise ConflictError("Database integrity error") from e
