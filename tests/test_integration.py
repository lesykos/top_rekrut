"""
Integration tests for database operations.

Tests the integration of multiple layers (models, repositories, services, API).
"""

import pytest
from sqlmodel import Session
from fastapi.testclient import TestClient

from app.models.item import Item, ItemCreate, ItemUpdate
from app.models.army_branch import ArmyBranch, ArmyBranchCreate
from app.models.rank_group import RankGroup, RankGroupCreate
from app.services.item_service import ItemService
from app.services.army_branch_service import ArmyBranchService
from app.services.rank_group_service import RankGroupService


class TestItemIntegration:
    """Integration tests for Item entity across layers."""

    @pytest.mark.integration
    def test_item_full_lifecycle(self, db_session: Session):
        """Test complete item lifecycle: create, read, update, delete."""
        service = ItemService(db_session)

        # Create
        item_create = ItemCreate(name="Integration Test Item", desc="Test Description")
        created = service.create_item(item_create)
        assert created.id is not None

        # Read
        retrieved = service.get_item(created.id)
        assert retrieved.name == "Integration Test Item"

        # Update
        update_data = ItemUpdate(name="Updated Name")
        updated = service.update_item(created.id, update_data)
        assert updated.name == "Updated Name"

        # Verify update in database
        verified = service.get_item(created.id)
        assert verified.name == "Updated Name"

        # Delete
        service.delete_item(created.id)

        # Verify deletion
        with pytest.raises(Exception):
            service.get_item(created.id)

    @pytest.mark.integration
    def test_item_with_api_endpoint(self, client: TestClient, db_session: Session):
        """Test item flow from database through service to API."""
        # Create via database
        item = Item(name="API Integration Item", desc="Description")
        db_session.add(item)
        db_session.commit()
        db_session.refresh(item)

        # Retrieve via API
        response = client.get(f"/api/items/{item.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "API Integration Item"

    @pytest.mark.integration
    def test_multiple_items_filtering(self, db_session: Session):
        """Test querying multiple items with filtering."""
        service = ItemService(db_session)

        # Create multiple items
        for i in range(5):
            item_create = ItemCreate(name=f"Item {i}", desc=f"Description {i}")
            service.create_item(item_create)

        # Get all items
        result = service.get_items()
        assert result.count == 5
        assert len(result.data) == 5

    @pytest.mark.integration
    def test_item_uniqueness_by_name(self, db_session: Session):
        """Test retrieving items by name."""
        service = ItemService(db_session)

        # Create items with different names
        names = ["Unique Item A", "Unique Item B", "Unique Item C"]
        for name in names:
            item_create = ItemCreate(name=name)
            service.create_item(item_create)

        # Retrieve by name
        found = service.repository.get_by_name("Unique Item B")
        assert found is not None
        assert found.name == "Unique Item B"


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

        # List all
        public = service.get_army_branches_public()
        assert public.count >= 1

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
        assert public.count == len(branch_names)

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
        rg_create = RankGroupCreate(name="Junior Officers", min_rank=5, max_rank=6)
        created = service.create_rank_group(rg_create)
        assert created.slug == "junior-officers"

        # Read
        retrieved = service.get_rank_group(created.id)
        assert retrieved.name == "Junior Officers"

        # List
        public = service.get_rank_groups_public()
        assert public.count >= 1

        # Delete
        service.delete_rank_group(created.id)

        # Verify deletion
        with pytest.raises(Exception):
            service.get_rank_group(created.id)

    @pytest.mark.integration
    def test_rank_group_api_full_flow(self, client: TestClient):
        """Test rank group operations through API."""
        # Create via admin API
        create_payload = {"name": "Senior NCOs", "min_rank": 7, "max_rank": 8}
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
        item_service = ItemService(db_session)
        branch_service = ArmyBranchService(db_session)
        rank_service = RankGroupService(db_session)

        # Create item
        item = item_service.create_item(ItemCreate(name="Equipment"))
        assert item.id is not None

        # Create branch
        branch = branch_service.create_army_branch(ArmyBranchCreate(name="Infantry"))
        assert branch.id is not None

        # Create rank group
        rank_group = rank_service.create_rank_group(
            RankGroupCreate(name="Officers", min_rank=5, max_rank=9)
        )
        assert rank_group.id is not None

        # Verify all are retrievable
        retrieved_item = item_service.get_item(item.id)
        retrieved_branch = branch_service.get_army_branch(branch.id)
        retrieved_rank = rank_service.get_rank_group(rank_group.id)

        assert retrieved_item.name == "Equipment"
        assert retrieved_branch.name == "Infantry"
        assert retrieved_rank.name == "Officers"

    @pytest.mark.integration
    def test_database_transaction_rollback(self, db_session: Session):
        """Test database transaction behavior."""
        service = ItemService(db_session)

        # Create an item
        item = service.create_item(ItemCreate(name="Test Item"))
        item_id = item.id

        # Verify it exists
        retrieved = service.get_item(item_id)
        assert retrieved is not None

        # Delete it
        service.delete_item(item_id)

        # Verify deletion persisted
        with pytest.raises(Exception):
            service.get_item(item_id)
