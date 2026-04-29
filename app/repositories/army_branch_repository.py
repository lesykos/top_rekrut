from typing import Any
from sqlmodel import select, col
from app.models.army_branch import ArmyBranch, ArmyBranchCreate, ArmyBranchUpdate
from .base import BaseRepository


class ArmyBranchRepository(BaseRepository[ArmyBranch]):

    def get_model_class(self) -> type[ArmyBranch]:
        return ArmyBranch

    # Get all army branches ordered by position.
    def get_all(self) -> Any:
        return self.session.exec(
            select(ArmyBranch).order_by(col(ArmyBranch.position).asc())
        ).all()

    # Get army branch by slug.
    def get_by_slug(self, slug: str) -> ArmyBranch | None:
        return self.session.exec(
            select(ArmyBranch).where(ArmyBranch.slug == slug)
        ).first()

    # Create ArmyBranch from ArmyBranchCreate data
    def create_from_data(self, army_branch_data: ArmyBranchCreate) -> ArmyBranch:
        army_branch = ArmyBranch(**army_branch_data.model_dump())
        return self.create(army_branch)

    # Update ArmyBranch from ArmyBranchUpdate data
    def update_from_data(
        self, army_branch: ArmyBranch, army_branch_data: ArmyBranchUpdate
    ) -> ArmyBranch:
        # Update fields:
        # exclude_unset - get only fields user provided
        update_dict = army_branch_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            # dynamically update DB object with new values
            setattr(army_branch, field, value)

        return self.update(army_branch)
