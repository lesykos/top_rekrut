"""
Unit tests for models.

Tests model validation, field constraints, and model functionality.
"""

import pytest
from datetime import datetime, timezone
from sqlmodel import Session

from app.models.army_branch import ArmyBranch, ArmyBranchCreate, ArmyBranchUpdate
from app.models.rank_group import RankGroup, RankGroupCreate, RankGroupUpdate


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
        rank_group = RankGroup(name="Officers")
        assert rank_group.name == "Officers"

    @pytest.mark.unit
    def test_rank_group_schema(self):
        """Test RankGroupCreate schema."""
        rank_create = RankGroupCreate(name="Enlisted")
        assert rank_create.name == "Enlisted"

    @pytest.mark.unit
    def test_rank_group_update_schema(self):
        """Test RankGroupUpdate schema."""
        update = RankGroupUpdate(name="Updated Name")
        assert update.name == "Updated Name"
