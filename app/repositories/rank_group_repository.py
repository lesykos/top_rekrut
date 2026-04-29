from typing import Sequence
from sqlmodel import select, col
from sqlalchemy.exc import IntegrityError
from app.core.exceptions import ValidationError, ConflictError
from app.models.rank_group import RankGroup, RankGroupCreate, RankGroupUpdate
from .base import BaseRepository


class RankGroupRepository(BaseRepository[RankGroup]):

    def get_model_class(self) -> type[RankGroup]:
        return RankGroup

    def get_all(self) -> Sequence[RankGroup]:
        """Get all RankGroups ordered by position."""
        return self.session.exec(
            select(RankGroup).order_by(col(RankGroup.position).asc())
        ).all()

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
                raise ValidationError("Key (slug) already exists.")

            raise ConflictError("Database integrity error")

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
                raise ValidationError("Key (slug) already exists.")

            raise ConflictError("Database integrity error")
