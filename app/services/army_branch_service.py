from typing import Sequence
from sqlmodel import Session
from app.core.exceptions import NotFoundError, BadRequestError
from app.models.army_branch import (
    ArmyBranch,
    ArmyBranchCreate,
    ArmyBranchUpdate,
    ArmyBranchPublic,
    ArmyBranchesPublic,
)
from app.repositories import ArmyBranchRepository
from .base import BaseService


class ArmyBranchService(BaseService[ArmyBranch]):
    """Service for army_branch business logic."""

    def __init__(self, session: Session):
        super().__init__(session)
        self.repository = ArmyBranchRepository(session)

    def count_army_branches(self, filter_: dict[str, str] | None = None) -> int:
        """Count ArmyBranches with optional filters."""
        return self.repository.count_all(filter_)

    def get_army_branch(self, army_branch_id: int) -> ArmyBranch:
        """Get ArmyBranch by ID"""
        army_branch = self.repository.get_by_id(army_branch_id)
        if army_branch is None:
            raise NotFoundError(f"Army branch {army_branch_id} not found")
        return army_branch

    def get_army_branch_by_slug(self, army_branch_slug: str) -> ArmyBranch:
        """Get ArmyBranch by slug"""
        army_branch = self.repository.get_by_slug(army_branch_slug)
        if not army_branch:
            raise NotFoundError(f"Army branch {army_branch_slug} not found")
        return army_branch

    def get_army_branches(
        self,
        sort: list[str] | None = None,
        range_: list[int] | None = None,
        filter_: dict[str, str] | None = None,
    ) -> Sequence[ArmyBranch]:
        """Get a list of ArmyBranches"""
        if range_ is not None:
            if len(range_) != 2:
                raise BadRequestError("Invalid query: range must be [start, end].")
            start, end = range_
            if start < 0 or end < start:
                raise BadRequestError("Invalid range bounds.")
            offset = start
            limit = end - start + 1
        else:
            offset = None
            limit = None
        return self.repository.get_all(sort, filter_, offset, limit)

    def get_army_branches_public(self) -> ArmyBranchesPublic:
        """Get a list of public ArmyBranches"""
        army_branches = self.repository.get_all()
        public = [ArmyBranchPublic.model_validate(branch) for branch in army_branches]
        return ArmyBranchesPublic(data=public, count=len(public))

    def create_army_branch(self, army_branch_data: ArmyBranchCreate) -> ArmyBranch:
        """Create new ArmyBranch with validation."""
        return self.repository.create_from_data(army_branch_data)

    def update_army_branch(
        self, army_branch_id: int, army_branch_data: ArmyBranchUpdate
    ) -> ArmyBranch:
        """Update existing ArmyBranch (by ID)"""
        existing_branch = self.get_army_branch(army_branch_id)
        return self.repository.update_from_data(existing_branch, army_branch_data)

    def update_army_branch_by_slug(
        self, army_branch_slug: str, army_branch_data: ArmyBranchUpdate
    ) -> ArmyBranch:
        """Update existing ArmyBranch (by slug)"""
        existing_branch = self.get_army_branch_by_slug(army_branch_slug)
        return self.repository.update_from_data(existing_branch, army_branch_data)

    def delete_army_branch(self, army_branch_id: int) -> None:
        """Delete existing ArmyBranch"""
        existing_branch = self.get_army_branch(army_branch_id)
        self.repository.delete(existing_branch)
