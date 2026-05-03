from typing import Sequence
from sqlmodel import select, col, func
from sqlalchemy.exc import IntegrityError
from app.core.exceptions import ValidationError, ConflictError
from app.models.army_unit import ArmyUnit, ArmyUnitCreate, ArmyUnitUpdate
from .base import BaseRepository

# from sqlalchemy.orm import joinedload


class ArmyUnitRepository(BaseRepository[ArmyUnit]):

    def get_model_class(self) -> type[ArmyUnit]:
        return ArmyUnit

    def count_all(self, filters: dict[str, str] | None = None) -> int:
        """Count all ArmyUnits with optional filters."""
        query = select(func.count()).select_from(ArmyUnit)
        if filters:
            if "id" in filters:
                query = query.where(col(ArmyUnit.id).in_(filters["id"]))
            if "name" in filters:
                query = query.where(col(ArmyUnit.name).ilike(f'%{filters["name"]}%'))
        return self.session.exec(query).one()

    def get_all(
        self,
        sort: list[str] | None = None,
        filters: dict[str, str] | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> Sequence[ArmyUnit]:
        """Get all ArmyUnits"""
        query = select(ArmyUnit)
        if filters:
            if "id" in filters:
                query = query.where(col(ArmyUnit.id).in_(filters["id"]))
            if "name" in filters:
                query = query.where(col(ArmyUnit.name).ilike(f'%{filters["name"]}%'))

        if sort:
            sort_field, sort_direction = sort
            column = getattr(ArmyUnit, sort_field)
            query = query.order_by(
                col(column).asc()
                if sort_direction.upper() == "ASC"
                else col(column).desc()
            )

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        return self.session.exec(query).all()

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
