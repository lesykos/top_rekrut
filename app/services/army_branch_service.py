from typing import List
from fastapi import HTTPException
from sqlmodel import Session
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

    def get_army_branch(self, army_branch_id: int) -> ArmyBranch | None:
        """Get ArmyBranch by ID"""
        try:
            army_branch = self.repository.get_by_id(army_branch_id)
            if not army_branch:
                raise HTTPException(status_code=404, detail="Army branch not found!")
            return army_branch

        except HTTPException:
            raise
        # Catch everything else (bugs) and handle/log them
        except Exception as e:
            self._handle_exception(e, f"get_army_branch({army_branch_id})")

    def get_army_branch_by_slug(self, army_branch_slug: str) -> ArmyBranch | None:
        """Get ArmyBranch by slug"""
        try:
            army_branch = self.repository.get_by_slug(army_branch_slug)
            if not army_branch:
                raise HTTPException(status_code=404, detail="Army branch not found!")
            return army_branch

        except HTTPException:
            raise
        except Exception as e:
            self._handle_exception(e, f"get_army_branch_by_slug({army_branch_slug})")

    def get_army_branches(self) -> List[ArmyBranch] | None:
        """Get a list of ArmyBranches"""
        try:
            army_branches = self.repository.get_all()
            return army_branches
        except Exception as e:
            self._handle_exception(e, "get_army_branches")

    def get_army_branches_public(self) -> ArmyBranchesPublic | None:
        """Get a list of public ArmyBranches"""
        try:
            army_branches = self.repository.get_all()
            army_branches_public = [
                ArmyBranchPublic.model_validate(branch) for branch in army_branches
            ]
            return ArmyBranchesPublic(
                data=army_branches_public, count=len(army_branches_public)
            )
        except Exception as e:
            self._handle_exception(e, "get_army_branches_public")

    def create_army_branch(
        self, army_branch_data: ArmyBranchCreate
    ) -> ArmyBranch | None:
        """Create new ArmyBranch with validation."""
        try:
            army_branch = self.repository.create_from_data(army_branch_data)
            return army_branch
        except HTTPException:
            raise
        except Exception as e:
            self._handle_exception(e, "create_army_branch")

    def update_army_branch(
        self, army_branch_slug: str, army_branch_data: ArmyBranchUpdate
    ) -> ArmyBranch | None:
        """Update existing ArmyBranch"""
        try:
            existing_branch = self.get_army_branch_by_slug(army_branch_slug)

            if existing_branch is not None:
                return self.repository.update_from_data(
                    existing_branch, army_branch_data
                )

        except HTTPException:
            raise
        except Exception as e:
            self._handle_exception(e, f"update_army_branch({army_branch_slug})")

    def delete_army_branch(self, army_branch_slug: str):
        """Delete existing ArmyBranch"""
        try:
            existing_branch = self.get_army_branch_by_slug(army_branch_slug)
            self.repository.delete(existing_branch) if existing_branch else None
        except HTTPException:
            raise
        except Exception as e:
            self._handle_exception(e, f"delete_army_branch({army_branch_slug})")
