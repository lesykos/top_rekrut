"""
Integration tests for database operations.

Tests the integration of multiple layers (models, repositories, services, API).
"""

import pytest
from sqlmodel import Session
from fastapi.testclient import TestClient

from app.models.army_branch import ArmyBranch, ArmyBranchCreate
from app.models.rank_group import RankGroup, RankGroupCreate
from app.services.army_branch_service import ArmyBranchService
from app.services.rank_group_service import RankGroupService


class TestArmyBranchIntegration:
    """Integration tests for ArmyBranch entity across layers."""

    @pytest.mark.integration
    def test_army_branch_full_lifecycle(self, db_session: Session):
        """Test complete army branch lifecycle."""
        service = ArmyBranchService(db_session)

        # Create with automatic slug generation
        branch_create = ArmyBranchCreate(name="Special Forces", position=2)
        created = service.create_army_branch(branch_create)
        assert created.slug == "special-forces"

        # Retrieve by ID
        retrieved = service.get_army_branch(created.id)
        assert retrieved.slug == "special-forces"

        # Retrieve by slug
        by_slug = service.get_army_branch_by_slug("special-forces")
        assert by_slug.id == created.id

        # Delete
        service.delete_army_branch(created.id)

        # Verify deletion
        with pytest.raises(Exception):
            service.get_army_branch(created.id)

    @pytest.mark.integration
    def test_army_branch_api_full_flow(self, client: TestClient, db_session: Session):
        """Test army branch operations through full API stack."""
        # Create via admin API
        create_payload = {"name": "Armor Corps", "position": 4}
        create_response = client.post("/api/admin/army-branches/", json=create_payload)
        assert create_response.status_code == 201
        branch_data = create_response.json()
        branch_id = branch_data["id"]

        # Read via admin API
        read_response = client.get(f"/api/admin/army-branches/{branch_id}")
        assert read_response.status_code == 200
        assert read_response.json()["name"] == "Armor Corps"

        # Update via admin API
        update_payload = {"position": 6}
        update_response = client.put(
            f"/api/admin/army-branches/{branch_id}", json=update_payload
        )
        assert update_response.status_code == 201
        assert update_response.json()["position"] == 6

        # Delete via admin API
        delete_response = client.delete(f"/api/admin/army-branches/{branch_id}")
        assert delete_response.status_code == 200

        # Verify deletion
        verify_response = client.get(f"/api/admin/army-branches/{branch_id}")
        assert verify_response.status_code == 404

    @pytest.mark.integration
    def test_army_branches_pagination(self, db_session: Session):
        """Test army branch pagination and sorting."""
        service = ArmyBranchService(db_session)

        # Create multiple branches
        branch_names = ["Infantry", "Cavalry", "Artillery", "Engineering", "Support"]
        for i, name in enumerate(branch_names, 1):
            branch_create = ArmyBranchCreate(name=name, position=i)
            service.create_army_branch(branch_create)

        # Get all branches
        public = service.get_army_branches_public()
        assert len(public.data) == len(branch_names)

        # Verify all branches are present
        names = [b.name for b in public.data]
        for expected_name in branch_names:
            assert expected_name in names

    @pytest.mark.integration
    def test_army_branch_slug_uniqueness(self, db_session: Session):
        """Test that branch slugs are unique."""
        service = ArmyBranchService(db_session)

        # Create first branch
        branch1 = ArmyBranchCreate(name="Special Forces")
        created1 = service.create_army_branch(branch1)

        # Try to create another with same slug (should fail)
        branch2 = ArmyBranchCreate(name="Special Forces", slug="special-forces")

        with pytest.raises(Exception):
            service.create_army_branch(branch2)


class TestRankGroupIntegration:
    """Integration tests for RankGroup entity across layers."""

    @pytest.mark.integration
    def test_rank_group_full_lifecycle(self, db_session: Session):
        """Test complete rank group lifecycle."""
        service = RankGroupService(db_session)

        # Create
        rg_create = RankGroupCreate(name="Junior Officers")
        created = service.create_rank_group(rg_create)
        assert created.slug == "junior-officers"

        # Read
        retrieved = service.get_rank_group(created.id)
        assert retrieved.name == "Junior Officers"

        # List
        public = service.get_rank_groups_public()
        assert len(public.data) >= 1

        # Delete
        service.delete_rank_group(created.id)

        # Verify deletion
        with pytest.raises(Exception):
            service.get_rank_group(created.id)

    @pytest.mark.integration
    def test_rank_group_api_full_flow(self, client: TestClient):
        """Test rank group operations through API."""
        # Create via admin API
        create_payload = {"name": "Senior NCOs"}
        create_response = client.post("/api/admin/rank-groups/", json=create_payload)
        assert create_response.status_code == 201
        rg_data = create_response.json()
        rg_id = rg_data["id"]

        # Read via admin API
        read_response = client.get(f"/api/admin/rank-groups/{rg_id}")
        assert read_response.status_code == 200

        # Delete via admin API
        delete_response = client.delete(f"/api/admin/rank-groups/{rg_id}")
        assert delete_response.status_code == 200


class TestCrossEntityIntegration:
    """Integration tests for relationships between entities."""

    @pytest.mark.integration
    def test_create_multiple_entity_types(self, db_session: Session):
        """Test creating multiple different entity types in sequence."""
        branch_service = ArmyBranchService(db_session)
        rank_service = RankGroupService(db_session)

        # Create branch
        branch = branch_service.create_army_branch(ArmyBranchCreate(name="Infantry"))
        assert branch.id is not None

        # Create rank group
        rank_group = rank_service.create_rank_group(RankGroupCreate(name="Officers"))
        assert rank_group.id is not None

        # Verify all are retrievable
        retrieved_branch = branch_service.get_army_branch(branch.id)
        retrieved_rank = rank_service.get_rank_group(rank_group.id)

        assert retrieved_branch.name == "Infantry"
        assert retrieved_rank.name == "Officers"
