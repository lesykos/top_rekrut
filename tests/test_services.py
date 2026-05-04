"""
Tests for service business logic.

Tests the business logic layer and service operations.
"""

import pytest
from sqlmodel import Session
from fastapi import HTTPException

from app.models.item import Item, ItemCreate, ItemUpdate
from app.models.army_branch import ArmyBranch, ArmyBranchCreate, ArmyBranchUpdate
from app.models.rank_group import RankGroup, RankGroupCreate, RankGroupUpdate
from app.services.item_service import ItemService
from app.services.army_branch_service import ArmyBranchService
from app.services.rank_group_service import RankGroupService
from app.core.exceptions import NotFoundError, ValidationError


class TestItemService:
    """Test suite for ItemService business logic."""

    @pytest.mark.unit
    def test_get_item_success(self, db_session: Session):
        """Test retrieving an item successfully."""
        service = ItemService(db_session)

        # Create an item first
        item = Item(name="Test Item", desc="Test")
        db_session.add(item)
        db_session.commit()
        db_session.refresh(item)

        # Get the item
        result = service.get_item(item.id)

        assert result.name == "Test Item"
        assert result.id == item.id

    @pytest.mark.unit
    def test_get_item_not_found(self, db_session: Session):
        """Test retrieving a non-existent item raises HTTPException."""
        service = ItemService(db_session)

        with pytest.raises(HTTPException) as exc_info:
            service.get_item(999)

        assert exc_info.value.status_code == 404

    @pytest.mark.unit
    def test_get_items_empty(self, db_session: Session):
        """Test getting items when none exist."""
        service = ItemService(db_session)

        result = service.get_items()

        assert result.count == 0
        assert len(result.data) == 0

    @pytest.mark.unit
    def test_get_items_multiple(self, db_session: Session):
        """Test getting multiple items."""
        service = ItemService(db_session)

        # Create items
        item1 = Item(name="Item 1")
        item2 = Item(name="Item 2")
        item3 = Item(name="Item 3")
        db_session.add(item1)
        db_session.add(item2)
        db_session.add(item3)
        db_session.commit()

        result = service.get_items()

        assert result.count == 3
        assert len(result.data) == 3


class TestArmyBranchService:
    """Test suite for ArmyBranchService business logic."""

    @pytest.mark.unit
    def test_get_army_branch_success(self, db_session: Session):
        """Test retrieving an army branch successfully."""
        service = ArmyBranchService(db_session)

        # Create a branch
        branch = ArmyBranch(name="Infantry", slug="infantry", position=1)
        db_session.add(branch)
        db_session.commit()
        db_session.refresh(branch)

        result = service.get_army_branch(branch.id)

        assert result.name == "Infantry"

    @pytest.mark.unit
    def test_get_army_branch_not_found(self, db_session: Session):
        """Test retrieving non-existent branch raises NotFoundError."""
        service = ArmyBranchService(db_session)

        with pytest.raises(NotFoundError):
            service.get_army_branch(999)

    @pytest.mark.unit
    def test_get_army_branch_by_slug(self, db_session: Session):
        """Test retrieving branch by slug."""
        service = ArmyBranchService(db_session)

        # Create a branch
        branch = ArmyBranch(name="Cavalry", slug="cavalry", position=2)
        db_session.add(branch)
        db_session.commit()

        result = service.get_army_branch_by_slug("cavalry")

        assert result.name == "Cavalry"

    @pytest.mark.unit
    def test_get_army_branch_by_slug_not_found(self, db_session: Session):
        """Test retrieving non-existent branch by slug."""
        service = ArmyBranchService(db_session)

        with pytest.raises(NotFoundError):
            service.get_army_branch_by_slug("nonexistent")

    @pytest.mark.unit
    def test_get_army_branches_empty(self, db_session: Session):
        """Test getting branches when none exist."""
        service = ArmyBranchService(db_session)

        result = service.get_army_branches_public()

        assert result.count == 0
        assert len(result.data) == 0

    @pytest.mark.unit
    def test_get_army_branches_multiple(self, db_session: Session):
        """Test getting multiple branches."""
        service = ArmyBranchService(db_session)

        # Create branches
        branch1 = ArmyBranch(name="Infantry", slug="infantry", position=1)
        branch2 = ArmyBranch(name="Cavalry", slug="cavalry", position=2)
        db_session.add(branch1)
        db_session.add(branch2)
        db_session.commit()

        result = service.get_army_branches_public()

        assert result.count == 2

    @pytest.mark.unit
    def test_create_army_branch(self, db_session: Session):
        """Test creating an army branch."""
        service = ArmyBranchService(db_session)
        branch_create = ArmyBranchCreate(name="Artillery")

        created_branch = service.create_army_branch(branch_create)

        assert created_branch.id is not None
        assert created_branch.name == "Artillery"
        assert created_branch.slug == "artillery"

    @pytest.mark.unit
    def test_update_army_branch(self, db_session: Session):
        """Test updating an army branch."""
        service = ArmyBranchService(db_session)

        # Create a branch
        branch = ArmyBranch(name="Infantry", slug="infantry", position=1)
        db_session.add(branch)
        db_session.commit()
        db_session.refresh(branch)

        # Update it
        update_data = ArmyBranchUpdate(position=3)
        updated_branch = service.update_army_branch(branch.id, update_data)

        assert updated_branch.position == 3

    @pytest.mark.unit
    def test_delete_army_branch(self, db_session: Session):
        """Test deleting an army branch."""
        service = ArmyBranchService(db_session)

        # Create a branch
        branch = ArmyBranch(name="Infantry", slug="infantry", position=1)
        db_session.add(branch)
        db_session.commit()
        db_session.refresh(branch)

        # Delete it
        service.delete_army_branch(branch.id)

        # Verify it's deleted
        with pytest.raises(NotFoundError):
            service.get_army_branch(branch.id)


class TestRankGroupService:
    """Test suite for RankGroupService business logic."""

    @pytest.mark.unit
    def test_get_rank_group_success(self, db_session: Session):
        """Test retrieving a rank group successfully."""
        service = RankGroupService(db_session)

        # Create a rank group
        rank_group = RankGroup(
            name="Officers", slug="officers", position=1, min_rank=5, max_rank=9
        )
        db_session.add(rank_group)
        db_session.commit()
        db_session.refresh(rank_group)

        result = service.get_rank_group(rank_group.id)

        assert result.name == "Officers"

    @pytest.mark.unit
    def test_get_rank_group_not_found(self, db_session: Session):
        """Test retrieving non-existent rank group."""
        service = RankGroupService(db_session)

        with pytest.raises(NotFoundError):
            service.get_rank_group(999)

    @pytest.mark.unit
    def test_get_rank_groups_empty(self, db_session: Session):
        """Test getting rank groups when none exist."""
        service = RankGroupService(db_session)

        result = service.get_rank_groups_public()

        assert result.count == 0

    @pytest.mark.unit
    def test_get_rank_groups_multiple(self, db_session: Session):
        """Test getting multiple rank groups."""
        service = RankGroupService(db_session)

        # Create rank groups
        rg1 = RankGroup(
            name="Officers", slug="officers", position=1, min_rank=5, max_rank=9
        )
        rg2 = RankGroup(
            name="Enlisted", slug="enlisted", position=2, min_rank=1, max_rank=4
        )
        db_session.add(rg1)
        db_session.add(rg2)
        db_session.commit()

        result = service.get_rank_groups_public()

        assert result.count == 2

    @pytest.mark.unit
    def test_create_rank_group(self, db_session: Session):
        """Test creating a rank group."""
        service = RankGroupService(db_session)
        rank_create = RankGroupCreate(name="NCOs", min_rank=4, max_rank=7)

        created = service.create_rank_group(rank_create)

        assert created.id is not None
        assert created.name == "NCOs"

    @pytest.mark.unit
    def test_delete_rank_group(self, db_session: Session):
        """Test deleting a rank group."""
        service = RankGroupService(db_session)

        # Create a rank group
        rank_group = RankGroup(
            name="Officers", slug="officers", position=1, min_rank=5, max_rank=9
        )
        db_session.add(rank_group)
        db_session.commit()
        db_session.refresh(rank_group)

        # Delete it
        service.delete_rank_group(rank_group.id)

        # Verify it's deleted
        with pytest.raises(NotFoundError):
            service.get_rank_group(rank_group.id)
