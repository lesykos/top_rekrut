from typing import List
from fastapi import HTTPException
from sqlmodel import Session
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

    def get_rank_group(self, rank_group_id: int) -> RankGroup | None:
        """Get RankGroup by ID"""
        try:
            rank_group = self.repository.get_by_id(rank_group_id)
            if not rank_group:
                raise HTTPException(status_code=404, detail="Rank group not found!")
            return rank_group

        except HTTPException:
            raise
        # Catch everything else (bugs) and handle/log them
        except Exception as e:
            self._handle_exception(e, f"get_rank_group({rank_group_id})")

    def get_rank_group_by_slug(self, rank_group_slug: str) -> RankGroup | None:
        """Get RankGroup by slug"""
        try:
            rank_group = self.repository.get_by_slug(rank_group_slug)
            if not rank_group:
                raise HTTPException(status_code=404, detail="Rank group not found!")
            return rank_group

        except HTTPException:
            raise
        except Exception as e:
            self._handle_exception(e, f"get_rank_group_by_slug({rank_group_slug})")

    def get_rank_groups(self) -> List[RankGroup] | None:
        """Get a list of RankGroups"""
        try:
            rank_groups = self.repository.get_all()
            return rank_groups
        except Exception as e:
            self._handle_exception(e, "get_rank_groups")

    def get_rank_groups_public(self) -> RankGroupsPublic | None:
        """Get a list of public RankGroups"""
        try:
            rank_groups = self.repository.get_all()
            rank_groups_public = [
                RankGroupPublic.model_validate(branch) for branch in rank_groups
            ]
            return RankGroupsPublic(
                data=rank_groups_public, count=len(rank_groups_public)
            )
        except Exception as e:
            self._handle_exception(e, "get_rank_groups_public")

    def create_rank_group(self, rank_group_data: RankGroupCreate) -> RankGroup | None:
        """Create new RankGroup"""
        try:
            rank_group = self.repository.create_from_data(rank_group_data)
            return rank_group
        except HTTPException:
            raise
        except Exception as e:
            self._handle_exception(e, "create_rank_group")

    def update_rank_group(
        self, rank_group_slug: str, rank_group_data: RankGroupUpdate
    ) -> RankGroup | None:
        """Update existing RankGroup"""
        try:
            existing_branch = self.get_rank_group_by_slug(rank_group_slug)

            if existing_branch is not None:
                return self.repository.update_from_data(
                    existing_branch, rank_group_data
                )

        except HTTPException:
            raise
        except Exception as e:
            self._handle_exception(e, f"update_rank_group({rank_group_slug})")

    def delete_rank_group(self, rank_group_slug: str):
        """Delete existing RankGroup"""
        try:
            existing_branch = self.get_rank_group_by_slug(rank_group_slug)
            self.repository.delete(existing_branch) if existing_branch else None
        except HTTPException:
            raise
        except Exception as e:
            self._handle_exception(e, f"delete_rank_group({rank_group_slug})")
