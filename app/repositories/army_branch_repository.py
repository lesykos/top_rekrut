from typing import Sequence
from sqlmodel import select, col
from sqlalchemy.exc import IntegrityError
from app.core.exceptions import ValidationError, ConflictError
from app.models.army_branch import ArmyBranch, ArmyBranchCreate, ArmyBranchUpdate
from .base import BaseRepository


class ArmyBranchRepository(BaseRepository[ArmyBranch]):

    def get_model_class(self) -> type[ArmyBranch]:
        return ArmyBranch

    def get_all(self) -> Sequence[ArmyBranch]:
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
        try:
            army_branch = ArmyBranch(**army_branch_data.model_dump())
            return self.create(army_branch)
        except IntegrityError as e:
            self.session.rollback()
            if "ix_army_branches_slug" in str(e.orig):
                raise ValidationError("Key (slug) already exists.")

            raise ConflictError("Database integrity error")

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
                raise ValidationError("Key (slug) already exists.")

            raise ConflictError("Database integrity error")
