from typing import Sequence
from sqlmodel import select, col, func
from sqlalchemy.exc import IntegrityError
from app.core.exceptions import ValidationError, ConflictError
from app.models.rank_group import RankGroup, RankGroupCreate, RankGroupUpdate
from .base import BaseRepository


class RankGroupRepository(BaseRepository[RankGroup]):

    def get_model_class(self) -> type[RankGroup]:
        return RankGroup

    def count_all(self, filters: dict[str, str] | None = None) -> int:
        """Count all RankGroups with optional filters."""
        query = select(func.count()).select_from(RankGroup)
        if filters:
            if "id" in filters:
                query = query.where(col(RankGroup.id).in_(filters["id"]))
            if "name" in filters:
                query = query.where(col(RankGroup.name).ilike(f'%{filters["name"]}%'))
        return self.session.exec(query).one()

    def get_all(
        self,
        sort: list[str] | None = None,
        filters: dict[str, str] | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> Sequence[RankGroup]:
        """Get all RankGroups"""
        query = select(RankGroup)
        if filters:
            if "id" in filters:
                query = query.where(col(RankGroup.id).in_(filters["id"]))
            if "name" in filters:
                query = query.where(col(RankGroup.name).ilike(f'%{filters["name"]}%'))

        if sort:
            sort_field, sort_direction = sort
            column = getattr(RankGroup, sort_field)
            query = query.order_by(
                col(column).asc()
                if sort_direction.upper() == "ASC"
                else col(column).desc()
            )
        else:
            query = query.order_by(col(RankGroup.position).asc())

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        return self.session.exec(query).all()

    def get_by_slug(self, slug: str) -> RankGroup | None:
        """Get RankGroup by slug."""
        return self.session.exec(
            select(RankGroup).where(RankGroup.slug == slug)
        ).first()

    def create_from_data(self, rank_group_data: RankGroupCreate) -> RankGroup:
        """Create RankGroup from RankGroupCreate data"""
        try:
            rank_group = RankGroup(**rank_group_data.model_dump())
            return self.create(rank_group)
        except IntegrityError as e:
            self.session.rollback()
            if "ix_rank_groups_slug" in str(e.orig):
                raise ValidationError("Key (slug) already exists.") from None

            raise ConflictError("Database integrity error") from e

    def update_from_data(
        self, rank_group: RankGroup, rank_group_data: RankGroupUpdate
    ) -> RankGroup:
        """Update RankGroup from RankGroupUpdate data"""
        try:
            # exclude_unset - get only fields user provided
            update_data = rank_group_data.model_dump(
                exclude_unset=True, exclude_none=True
            )
            rank_group.sqlmodel_update(update_data)
            return self.update(rank_group)
        except IntegrityError as e:
            self.session.rollback()
            if "ix_rank_groups_slug" in str(e.orig):
                raise ValidationError("Key (slug) already exists.") from None

            raise ConflictError("Database integrity error") from e
