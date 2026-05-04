from typing import Sequence
from sqlmodel import select, col, func
from sqlalchemy.exc import IntegrityError
from app.core.exceptions import ValidationError, ConflictError
from app.models.army_branch import ArmyBranch, ArmyBranchCreate, ArmyBranchUpdate
from .base import BaseRepository


class ArmyBranchRepository(BaseRepository[ArmyBranch]):

    def get_model_class(self) -> type[ArmyBranch]:
        return ArmyBranch

    def count_all(self, filters: dict[str, str] | None = None) -> int:
        """Count all army branches with optional filters."""
        query = select(func.count()).select_from(ArmyBranch)
        query = self.admin_query_filters(query, filters)
        return self.session.exec(query).one()

    def get_all(
        self,
        sort: list[str] | None = None,
        filters: dict[str, str] | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> Sequence[ArmyBranch]:
        """Get all army branches"""
        query = select(ArmyBranch)
        query = self.admin_query_filters(query, filters)
        query = self.admin_query_sort(query, sort)

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        return self.session.exec(query).all()

    def get_by_slug(self, slug: str) -> ArmyBranch | None:
        """Get ArmyBranch by slug."""
        return self.session.exec(
            select(ArmyBranch).where(ArmyBranch.slug == slug)
        ).first()

    def create_from_data(self, army_branch_data: ArmyBranchCreate) -> ArmyBranch:
        """Create ArmyBranch from ArmyBranchCreate data"""
        try:
            army_branch = ArmyBranch(**army_branch_data.model_dump())
            return self.create(army_branch)
        except IntegrityError as e:
            self.session.rollback()
            if "ix_army_branches_slug" in str(e.orig):
                raise ValidationError("Key (slug) already exists.") from None

            raise ConflictError("Database integrity error") from e

    def update_from_data(
        self, army_branch: ArmyBranch, army_branch_data: ArmyBranchUpdate
    ) -> ArmyBranch:
        """Update ArmyBranch from ArmyBranchUpdate data"""
        try:
            # exclude_unset - get only fields user provided
            update_data = army_branch_data.model_dump(
                exclude_unset=True, exclude_none=True
            )
            army_branch.sqlmodel_update(update_data)
            return self.update(army_branch)
        except IntegrityError as e:
            self.session.rollback()
            if "ix_army_branches_slug" in str(e.orig):
                raise ValidationError("Key (slug) already exists.") from None

            raise ConflictError("Database integrity error") from e

    def admin_query_filters(self, query, filters):
        if filters:
            for field in ["id"]:
                if field in filters:
                    column = getattr(ArmyBranch, field)
                    query = query.where(col(column).in_(filters[field]))
            if "name" in filters:
                query = query.where(col(ArmyBranch.name).ilike(f'%{filters["name"]}%'))
        return query

    def admin_query_sort(self, query, sort):
        if sort:
            sort_field, sort_direction = sort
            column = getattr(ArmyBranch, sort_field)
            query = query.order_by(
                col(column).asc()
                if sort_direction.upper() == "ASC"
                else col(column).desc()
            )
        else:
            query = query.order_by(col(ArmyBranch.position).asc())

        return query
