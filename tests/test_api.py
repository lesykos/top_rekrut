"""
Tests for API endpoints.

Tests the API routes and HTTP responses.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.item import Item, ItemCreate
from app.models.army_branch import ArmyBranch, ArmyBranchCreate
from app.models.rank_group import RankGroup, RankGroupCreate


class TestItemEndpoints:
    """Test suite for Item API endpoints."""

    @pytest.mark.api
    def test_read_items_empty(self, client: TestClient):
        """Test reading items when none exist."""
        response = client.get("/api/items/")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0
        assert data["data"] == []

    @pytest.mark.api
    def test_read_items_multiple(self, client: TestClient, db_session: Session):
        """Test reading multiple items."""
        # Create items in database
        item1 = Item(name="Item 1")
        item2 = Item(name="Item 2")
        db_session.add(item1)
        db_session.add(item2)
        db_session.commit()

        response = client.get("/api/items/")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 2
        assert len(data["data"]) == 2

    @pytest.mark.api
    def test_read_item_by_id(self, client: TestClient, db_session: Session):
        """Test reading a specific item by ID."""
        # Create an item
        item = Item(name="Test Item", desc="Test Description")
        db_session.add(item)
        db_session.commit()
        db_session.refresh(item)

        response = client.get(f"/api/items/{item.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Item"
        assert data["id"] == item.id

    @pytest.mark.api
    def test_read_item_not_found(self, client: TestClient):
        """Test reading a non-existent item returns 404."""
        response = client.get("/api/items/999")

        assert response.status_code == 404


class TestArmyBranchEndpoints:
    """Test suite for ArmyBranch API endpoints."""

    @pytest.mark.api
    def test_get_army_branches_empty(self, client: TestClient):
        """Test getting army branches when none exist."""
        response = client.get("/api/army-branches/")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0
        assert data["data"] == []

    @pytest.mark.api
    def test_get_army_branches_multiple(self, client: TestClient, db_session: Session):
        """Test getting multiple army branches."""
        # Create branches
        branch1 = ArmyBranch(name="Infantry", slug="infantry", position=1)
        branch2 = ArmyBranch(name="Cavalry", slug="cavalry", position=2)
        db_session.add(branch1)
        db_session.add(branch2)
        db_session.commit()

        response = client.get("/api/army-branches/")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 2
        assert len(data["data"]) == 2

    @pytest.mark.api
    def test_get_army_branch_by_id(self, client: TestClient, db_session: Session):
        """Test getting a specific army branch by ID."""
        # Create a branch
        branch = ArmyBranch(name="Infantry", slug="infantry", position=1)
        db_session.add(branch)
        db_session.commit()
        db_session.refresh(branch)

        response = client.get(f"/api/army-branches/{branch.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Infantry"

    @pytest.mark.api
    def test_get_army_branch_not_found(self, client: TestClient):
        """Test getting non-existent army branch returns 404."""
        response = client.get("/api/army-branches/999")

        assert response.status_code == 404

    @pytest.mark.api
    def test_create_army_branch(self, client: TestClient):
        """Test creating a new army branch via admin endpoint."""
        payload = {"name": "Artillery", "position": 3}

        response = client.post("/api/admin/army-branches/", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Artillery"
        assert data["slug"] == "artillery"
        assert data["position"] == 3

    @pytest.mark.api
    def test_create_army_branch_duplicate_slug(
        self, client: TestClient, db_session: Session
    ):
        """Test creating army branch with duplicate slug returns error."""
        # Create first branch
        branch = ArmyBranch(name="Infantry", slug="infantry", position=1)
        db_session.add(branch)
        db_session.commit()

        # Try to create another with same slug
        payload = {"name": "Infantry Unit", "slug": "infantry", "position": 2}

        response = client.post("/api/admin/army-branches/", json=payload)

        assert response.status_code == 409

    @pytest.mark.api
    def test_update_army_branch(self, client: TestClient, db_session: Session):
        """Test updating an army branch via admin endpoint."""
        # Create a branch
        branch = ArmyBranch(name="Infantry", slug="infantry", position=1)
        db_session.add(branch)
        db_session.commit()
        db_session.refresh(branch)

        payload = {"position": 5}

        response = client.put(f"/api/admin/army-branches/{branch.id}", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["position"] == 5

    @pytest.mark.api
    def test_delete_army_branch(self, client: TestClient, db_session: Session):
        """Test deleting an army branch via admin endpoint."""
        # Create a branch
        branch = ArmyBranch(name="Infantry", slug="infantry", position=1)
        db_session.add(branch)
        db_session.commit()
        db_session.refresh(branch)

        response = client.delete(f"/api/admin/army-branches/{branch.id}")

        assert response.status_code == 200

        # Verify it's deleted
        get_response = client.get(f"/api/admin/army-branches/{branch.id}")
        assert get_response.status_code == 404


class TestRankGroupEndpoints:
    """Test suite for RankGroup API endpoints."""

    @pytest.mark.api
    def test_get_rank_groups_empty(self, client: TestClient):
        """Test getting rank groups when none exist."""
        response = client.get("/api/rank-groups/")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0

    @pytest.mark.api
    def test_get_rank_groups_multiple(self, client: TestClient, db_session: Session):
        """Test getting multiple rank groups."""
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

        response = client.get("/api/rank-groups/")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 2

    @pytest.mark.api
    def test_create_rank_group(self, client: TestClient):
        """Test creating a new rank group via admin endpoint."""
        payload = {"name": "NCOs", "min_rank": 4, "max_rank": 7}

        response = client.post("/api/admin/rank-groups/", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "NCOs"
        assert data["slug"] == "ncos"

    @pytest.mark.api
    def test_delete_rank_group(self, client: TestClient, db_session: Session):
        """Test deleting a rank group via admin endpoint."""
        # Create a rank group
        rg = RankGroup(
            name="Officers", slug="officers", position=1, min_rank=5, max_rank=9
        )
        db_session.add(rg)
        db_session.commit()
        db_session.refresh(rg)

        response = client.delete(f"/api/admin/rank-groups/{rg.id}")

        assert response.status_code == 200

        # Verify it's deleted
        get_response = client.get(f"/api/admin/rank-groups/{rg.id}")
        assert get_response.status_code == 404


class TestUtilsEndpoints:
    """Test utility endpoints and shared API helpers."""

    @pytest.mark.api
    def test_health_check(self, client: TestClient):
        response = client.get("/api/utils/health-check/")
        assert response.status_code == 200
        assert response.json() is True


class TestAdminQueryParams:
    """Test internal query parameter handling for admin endpoints."""

    @pytest.mark.api
    def test_army_branch_admin_query_params(
        self, client: TestClient, db_session: Session
    ):
        # Create several branches
        branches = [
            ArmyBranch(name="Infantry", slug="infantry", position=1),
            ArmyBranch(name="Cavalry", slug="cavalry", position=2),
            ArmyBranch(name="Artillery", slug="artillery", position=3),
        ]
        for branch in branches:
            db_session.add(branch)
        db_session.commit()

        response = client.get(
            '/api/admin/army-branches/?sort=["position", "DESC"]&range=[0,1]'
        )
        assert response.status_code == 200
        assert response.headers["Content-Range"].startswith("army-branches")
        data = response.json()
        assert data["count"] == 3
        assert len(data["data"]) == 2

    @pytest.mark.api
    def test_rank_group_admin_query_params(
        self, client: TestClient, db_session: Session
    ):
        rank_groups = [
            RankGroup(
                name="Officers", slug="officers", position=1, min_rank=5, max_rank=9
            ),
            RankGroup(
                name="Enlisted", slug="enlisted", position=2, min_rank=1, max_rank=4
            ),
            RankGroup(
                name="Special", slug="special", position=3, min_rank=7, max_rank=9
            ),
        ]
        for rg in rank_groups:
            db_session.add(rg)
        db_session.commit()

        response = client.get(
            '/api/admin/rank-groups/?sort=["position", "ASC"]&range=[1,2]&filter={"id":[1,2,3]}'
        )
        assert response.status_code == 200
        assert response.headers["Content-Range"].startswith("rank-groups")
        data = response.json()
        assert data["count"] == 3
        assert len(data["data"]) == 2
