from typing import Any
from sqlmodel import select, col
from app.models.army_branch import ArmyBranch, ArmyBranchCreate, ArmyBranchUpdate
from .base import BaseRepository


class ArmyBranchRepository(BaseRepository[ArmyBranch]):

    def get_model_class(self) -> type[ArmyBranch]:
        return ArmyBranch

    def get_all(self) -> Any:
        """Get all army branches ordered by position."""
        return self.session.exec(
            select(ArmyBranch).order_by(col(ArmyBranch.position).asc())
        ).all()

    def get_by_slug(self, slug: str) -> ArmyBranch | None:
        """Get army branch by slug."""
        return self.session.exec(
            select(ArmyBranch).where(ArmyBranch.slug == slug)
        ).first()

    def create_from_data(self, army_branch_data: ArmyBranchCreate) -> ArmyBranch:
        """Create ArmyBranch from ArmyBranchCreate data"""
        army_branch = ArmyBranch(**army_branch_data.model_dump())
        return self.create(army_branch)

    def update_from_data(
        self, army_branch: ArmyBranch, army_branch_data: ArmyBranchUpdate
    ) -> ArmyBranch:
        """Update ArmyBranch from ArmyBranchUpdate data"""
        # Update fields:
        # exclude_unset - get only fields user provided
        update_dict = army_branch_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            # dynamically update DB object with new values
            setattr(army_branch, field, value)

        return self.update(army_branch)
