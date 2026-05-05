"""
Tests for repository CRUD operations.

Tests the data access layer and repository pattern implementation.
"""

import pytest
from sqlmodel import Session

from app.models.army_branch import ArmyBranch, ArmyBranchCreate
from app.models.rank_group import RankGroup, RankGroupCreate
from app.repositories.army_branch_repository import ArmyBranchRepository
from app.repositories.rank_group_repository import RankGroupRepository


class TestArmyBranchRepository:
    """Test suite for ArmyBranchRepository CRUD operations."""

    @pytest.mark.unit
    def test_create_army_branch(self, db_session: Session):
        """Test creating an army branch."""
        repo = ArmyBranchRepository(db_session)
        branch = ArmyBranch(name="Infantry", slug="infantry", position=1)

        created_branch = repo.create(branch)

        assert created_branch.id is not None
        assert created_branch.name == "Infantry"
        assert created_branch.slug == "infantry"

    @pytest.mark.unit
    def test_get_army_branch_by_id(self, db_session: Session):
        """Test retrieving army branch by ID."""
        repo = ArmyBranchRepository(db_session)
        branch = ArmyBranch(name="Infantry", slug="infantry", position=1)
        created_branch = repo.create(branch)

        retrieved_branch = repo.get_by_id(created_branch.id)

        assert retrieved_branch is not None
        assert retrieved_branch.slug == "infantry"

    @pytest.mark.unit
    def test_get_all_army_branches(self, db_session: Session):
        """Test retrieving all army branches."""
        repo = ArmyBranchRepository(db_session)

        branch1 = repo.create(ArmyBranch(name="Infantry", slug="infantry", position=1))
        branch2 = repo.create(ArmyBranch(name="Cavalry", slug="cavalry", position=2))

        all_branches = repo.get_all()

        assert len(all_branches) == 2

    @pytest.mark.unit
    def test_update_army_branch(self, db_session: Session):
        """Test updating an army branch."""
        repo = ArmyBranchRepository(db_session)
        branch = ArmyBranch(name="Infantry", slug="infantry", position=1)
        created_branch = repo.create(branch)

        created_branch.position = 5
        updated_branch = repo.update(created_branch)

        assert updated_branch.position == 5

    @pytest.mark.unit
    def test_delete_army_branch(self, db_session: Session):
        """Test deleting an army branch."""
        repo = ArmyBranchRepository(db_session)
        branch = ArmyBranch(name="Infantry", slug="infantry", position=1)
        created_branch = repo.create(branch)

        repo.delete(created_branch)

        retrieved_branch = repo.get_by_id(created_branch.id)
        assert retrieved_branch is None

    @pytest.mark.unit
    def test_get_army_branch_by_slug(self, db_session: Session):
        """Test retrieving army branch by slug."""
        repo = ArmyBranchRepository(db_session)
        branch = ArmyBranch(name="Infantry", slug="infantry", position=1)
        repo.create(branch)

        found_branch = repo.get_by_slug("infantry")

        assert found_branch is not None
        assert found_branch.slug == "infantry"

    @pytest.mark.unit
    def test_army_branch_exists(self, db_session: Session):
        """Test checking if army branch exists."""
        repo = ArmyBranchRepository(db_session)
        branch = ArmyBranch(name="Infantry", slug="infantry", position=1)
        created_branch = repo.create(branch)

        exists = repo.exists(created_branch.id)

        assert exists is True


class TestRankGroupRepository:
    """Test suite for RankGroupRepository CRUD operations."""

    @pytest.mark.unit
    def test_create_rank_group(self, db_session: Session):
        """Test creating a rank group."""
        repo = RankGroupRepository(db_session)
        rank_group = RankGroup(name="Officers", slug="officers", position=1)

        created = repo.create(rank_group)

        assert created.id is not None
        assert created.name == "Officers"

    @pytest.mark.unit
    def test_get_rank_group_by_id(self, db_session: Session):
        """Test retrieving rank group by ID."""
        repo = RankGroupRepository(db_session)
        rank_group = RankGroup(name="Officers", slug="officers", position=1)
        created = repo.create(rank_group)

        retrieved = repo.get_by_id(created.id)

        assert retrieved is not None
        assert retrieved.name == "Officers"

    @pytest.mark.unit
    def test_get_all_rank_groups(self, db_session: Session):
        """Test retrieving all rank groups."""
        repo = RankGroupRepository(db_session)

        repo.create(RankGroup(name="Officers", slug="officers", position=1))
        repo.create(RankGroup(name="Enlisted", slug="enlisted", position=2))

        all_groups = repo.get_all()

        assert len(all_groups) == 2

    @pytest.mark.unit
    def test_update_rank_group(self, db_session: Session):
        """Test updating a rank group."""
        repo = RankGroupRepository(db_session)
        rank_group = RankGroup(name="Officers", slug="officers", position=1)
        created = repo.create(rank_group)

        created.position = 3
        updated = repo.update(created)

        assert updated.position == 3

    @pytest.mark.unit
    def test_delete_rank_group(self, db_session: Session):
        """Test deleting a rank group."""
        repo = RankGroupRepository(db_session)
        rank_group = RankGroup(name="Officers", slug="officers", position=1)
        created = repo.create(rank_group)

        repo.delete(created)

        retrieved = repo.get_by_id(created.id)
        assert retrieved is None

    @pytest.mark.unit
    def test_rank_group_exists(self, db_session: Session):
        """Test checking if rank group exists."""
        repo = RankGroupRepository(db_session)
        rank_group = RankGroup(name="Officers", slug="officers", position=1)
        created = repo.create(rank_group)

        exists = repo.exists(created.id)

        assert exists is True
