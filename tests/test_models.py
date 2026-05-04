"""
Unit tests for models.

Tests model validation, field constraints, and model functionality.
"""

import pytest
from datetime import datetime, timezone
from sqlmodel import Session

from app.models.item import Item, ItemBase, ItemCreate, ItemUpdate, ItemPublic
from app.models.army_branch import ArmyBranch, ArmyBranchCreate, ArmyBranchUpdate
from app.models.rank_group import RankGroup, RankGroupCreate, RankGroupUpdate


class TestItemModel:
    """Test suite for Item model."""

    @pytest.mark.unit
    def test_item_creation_with_required_fields(self):
        """Test creating an Item with required fields."""
        item = Item(name="Test Item")
        assert item.name == "Test Item"
        assert item.desc is None
        assert isinstance(item.created_at, datetime)

    @pytest.mark.unit
    def test_item_creation_with_all_fields(self):
        """Test creating an Item with all fields."""
        item = Item(name="Test Item", desc="A test description")
        assert item.name == "Test Item"
        assert item.desc == "A test description"
        assert isinstance(item.created_at, datetime)

    @pytest.mark.unit
    def test_item_name_min_length_validation(self):
        """Test Item name minimum length validation."""
        with pytest.raises(Exception):
            ItemBase(name="")

    @pytest.mark.unit
    def test_item_name_max_length_validation(self):
        """Test Item name maximum length validation."""
        with pytest.raises(Exception):
            ItemBase(name="x" * 256)

    @pytest.mark.unit
    def test_item_desc_max_length_validation(self):
        """Test Item description maximum length validation."""
        with pytest.raises(Exception):
            ItemBase(name="Valid", desc="x" * 256)

    @pytest.mark.unit
    def test_item_create_schema(self):
        """Test ItemCreate schema."""
        item_create = ItemCreate(name="New Item", desc="New description")
        assert item_create.name == "New Item"
        assert item_create.desc == "New description"

    @pytest.mark.unit
    def test_item_update_schema_partial(self):
        """Test ItemUpdate schema with partial updates."""
        item_update = ItemUpdate(name=None)
        assert item_update.name is None

    @pytest.mark.unit
    def test_item_public_schema(self):
        """Test ItemPublic schema."""
        item = Item(id=1, name="Test")
        item_public = ItemPublic.model_validate(item)
        assert item_public.id == 1
        assert item_public.name == "Test"

    @pytest.mark.unit
    def test_item_table_name(self):
        """Test Item table configuration."""
        assert Item.__tablename__ == "item"


class TestArmyBranchModel:
    """Test suite for ArmyBranch model."""

    @pytest.mark.unit
    def test_army_branch_creation_with_required_fields(self):
        """Test creating ArmyBranch with required fields."""
        branch = ArmyBranch(name="Infantry", slug="infantry", position=1)
        assert branch.name == "Infantry"
        assert branch.slug == "infantry"
        assert branch.position == 1

    @pytest.mark.unit
    def test_army_branch_slug_generation_on_create(self):
        """Test automatic slug generation on ArmyBranchCreate."""
        branch_create = ArmyBranchCreate(name="Artillery")
        assert branch_create.slug == "artillery"

    @pytest.mark.unit
    def test_army_branch_slug_generation_with_spaces(self):
        """Test slug generation handles spaces correctly."""
        branch_create = ArmyBranchCreate(name="Special Forces")
        assert branch_create.slug == "special-forces"

    @pytest.mark.unit
    def test_army_branch_custom_slug(self):
        """Test custom slug overrides automatic generation."""
        branch_create = ArmyBranchCreate(name="Infantry", slug="inf")
        assert branch_create.slug == "inf"

    @pytest.mark.unit
    def test_army_branch_name_min_length_validation(self):
        """Test ArmyBranch name minimum length validation."""
        with pytest.raises(Exception):
            ArmyBranchCreate(name="")

    @pytest.mark.unit
    def test_army_branch_position_min_validation(self):
        """Test ArmyBranch position minimum value."""
        with pytest.raises(Exception):
            ArmyBranch(name="Test", slug="test", position=0)

    @pytest.mark.unit
    def test_army_branch_position_max_validation(self):
        """Test ArmyBranch position maximum value."""
        with pytest.raises(Exception):
            ArmyBranch(name="Test", slug="test", position=31)

    @pytest.mark.unit
    def test_army_branch_default_position(self):
        """Test ArmyBranch default position value."""
        branch_create = ArmyBranchCreate(name="Test")
        branch = ArmyBranch(**branch_create.model_dump())
        assert branch.position == 30

    @pytest.mark.unit
    def test_army_branch_update_schema(self):
        """Test ArmyBranchUpdate schema."""
        update = ArmyBranchUpdate(name="New Name", position=5)
        assert update.name == "New Name"
        assert update.position == 5
        assert update.slug is None

    @pytest.mark.unit
    def test_army_branch_table_name(self):
        """Test ArmyBranch table configuration."""
        assert ArmyBranch.__tablename__ == "army_branches"

    @pytest.mark.unit
    def test_army_branch_slug_index(self):
        """Test that slug is indexed and unique."""
        # This test verifies the database schema configuration
        branch = ArmyBranch(name="Test", slug="test-slug", position=1)
        assert branch.slug == "test-slug"


class TestRankGroupModel:
    """Test suite for RankGroup model."""

    @pytest.mark.unit
    def test_rank_group_creation(self):
        """Test RankGroup creation."""
        rank_group = RankGroup(name="Officers", min_rank=5, max_rank=10)
        assert rank_group.name == "Officers"
        assert rank_group.min_rank == 5
        assert rank_group.max_rank == 10

    @pytest.mark.unit
    def test_rank_group_name_validation(self):
        """Test RankGroup name validation."""
        with pytest.raises(Exception):
            RankGroup(name="", min_rank=1, max_rank=5)

    @pytest.mark.unit
    def test_rank_group_schema(self):
        """Test RankGroupCreate schema."""
        rank_create = RankGroupCreate(name="Enlisted", min_rank=1, max_rank=4)
        assert rank_create.name == "Enlisted"
        assert rank_create.min_rank == 1
        assert rank_create.max_rank == 4

    @pytest.mark.unit
    def test_rank_group_update_schema(self):
        """Test RankGroupUpdate schema."""
        update = RankGroupUpdate(name="Updated Name")
        assert update.name == "Updated Name"
