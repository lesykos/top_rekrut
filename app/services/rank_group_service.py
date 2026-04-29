from typing import Sequence
from sqlmodel import Session
from app.core.exceptions import NotFoundError
from app.models.rank_group import (
    RankGroup,
    RankGroupCreate,
    RankGroupUpdate,
    RankGroupPublic,
    RankGroupsPublic,
)
from app.repositories import RankGroupRepository
from .base import BaseService


class RankGroupService(BaseService[RankGroup]):
    """Service for RankGroup business logic."""

    def __init__(self, session: Session):
        super().__init__(session)
        self.repository = RankGroupRepository(session)

    def get_rank_group(self, rank_group_id: int) -> RankGroup:
        """Get RankGroup by ID"""
        rank_group = self.repository.get_by_id(rank_group_id)
        if rank_group is None:
            raise NotFoundError(f"Rank group {rank_group_id} not found")
        return rank_group

    def get_rank_group_by_slug(self, rank_group_slug: str) -> RankGroup:
        """Get RankGroup by slug"""
        rank_group = self.repository.get_by_slug(rank_group_slug)
        if rank_group is None:
            raise NotFoundError(f"Rank group {rank_group_slug} not found")
        return rank_group

    def get_rank_groups(self) -> Sequence[RankGroup]:
        """Get a list of RankGroups"""
        return self.repository.get_all()

    def get_rank_groups_public(self) -> RankGroupsPublic:
        """Get a list of public RankGroups"""
        rank_groups = self.repository.get_all()
        rank_groups_public = [
            RankGroupPublic.model_validate(rank_group) for rank_group in rank_groups
        ]
        return RankGroupsPublic(data=rank_groups_public, count=len(rank_groups_public))

    def create_rank_group(self, rank_group_data: RankGroupCreate) -> RankGroup:
        """Create new RankGroup"""
        return self.repository.create_from_data(rank_group_data)

    def update_rank_group(
        self, rank_group_slug: str, rank_group_data: RankGroupUpdate
    ) -> RankGroup:
        """Update existing RankGroup"""
        existing_rank_group = self.get_rank_group_by_slug(rank_group_slug)
        return self.repository.update_from_data(existing_rank_group, rank_group_data)

    def delete_rank_group(self, rank_group_slug: str) -> None:
        """Delete existing RankGroup"""
        existing_rank_group = self.get_rank_group_by_slug(rank_group_slug)
        self.repository.delete(existing_rank_group)
