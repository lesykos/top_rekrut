"""
Tests for ArmyUnit model, repository, service, and API endpoints.
"""

import pytest
from sqlmodel import Session
from fastapi.testclient import TestClient

from app.models.army_unit import ArmyUnit, ArmyUnitCreate, ArmyUnitUpdate
from app.repositories.army_unit_repository import ArmyUnitRepository
from app.services.army_unit_service import ArmyUnitService


class TestArmyUnitModel:
    @pytest.mark.unit
    def test_army_unit_slug_generation(self):
        data = ArmyUnitCreate(name="Armored Division")
        assert data.slug == "armored-division"

    @pytest.mark.unit
    def test_army_unit_website_serialization(self):
        data = ArmyUnitCreate(name="Engineers", website="https://example.com")
        assert data.website in {"https://example.com", "https://example.com/"}

    @pytest.mark.unit
    def test_army_unit_name_validation(self):
        with pytest.raises(Exception):
            ArmyUnitCreate(name="")

    @pytest.mark.unit
    def test_army_unit_max_length_validation(self):
        with pytest.raises(Exception):
            ArmyUnitCreate(name="x" * 256)


class TestArmyUnitRepository:
    @pytest.mark.unit
    def test_create_and_get_army_unit(self, db_session: Session):
        repo = ArmyUnitRepository(db_session)
        army_unit = ArmyUnit(name="Infantry Unit", slug="infantry-unit")
        created = repo.create(army_unit)
        assert created.id is not None
        assert created.slug == "infantry-unit"

        from_db = repo.get_by_id(created.id)
        assert from_db is not None
        assert from_db.name == "Infantry Unit"

    @pytest.mark.unit
    def test_get_by_slug(self, db_session: Session):
        repo = ArmyUnitRepository(db_session)
        army_unit = ArmyUnit(name="Recon", slug="recon")
        repo.create(army_unit)

        found = repo.get_by_slug("recon")
        assert found is not None
        assert found.name == "Recon"

    @pytest.mark.unit
    def test_update_army_unit(self, db_session: Session):
        repo = ArmyUnitRepository(db_session)
        army_unit = ArmyUnit(name="Recon", slug="recon")
        created = repo.create(army_unit)
        created.name = "Recon Updated"
        updated = repo.update(created)
        assert updated.name == "Recon Updated"

    @pytest.mark.unit
    def test_delete_army_unit(self, db_session: Session):
        repo = ArmyUnitRepository(db_session)
        army_unit = ArmyUnit(name="Tanks", slug="tanks")
        created = repo.create(army_unit)
        repo.delete(created)
        assert repo.get_by_id(created.id) is None


class TestArmyUnitService:
    @pytest.mark.unit
    def test_get_army_unit_not_found(self, db_session: Session):
        service = ArmyUnitService(db_session)
        with pytest.raises(Exception):
            service.get_army_unit(999)

    @pytest.mark.unit
    def test_create_army_unit(self, db_session: Session):
        service = ArmyUnitService(db_session)
        created = service.create_army_unit(ArmyUnitCreate(name="Support Unit"))
        assert created.id is not None
        assert created.slug == "support-unit"

    @pytest.mark.unit
    def test_update_army_unit(self, db_session: Session):
        service = ArmyUnitService(db_session)
        created = service.create_army_unit(ArmyUnitCreate(name="Logistics"))
        updated = service.update_army_unit(
            created.id, ArmyUnitUpdate(name="Logistics Team")
        )
        assert updated.name == "Logistics Team"

    @pytest.mark.unit
    def test_delete_army_unit(self, db_session: Session):
        service = ArmyUnitService(db_session)
        created = service.create_army_unit(ArmyUnitCreate(name="Cavalry"))
        service.delete_army_unit(created.id)
        with pytest.raises(Exception):
            service.get_army_unit(created.id)


class TestArmyUnitApiEndpoints:
    @pytest.mark.api
    def test_create_and_get_army_unit_via_api(self, client: TestClient):
        payload = {"name": "Signal Corps"}
        response = client.post("/api/admin/army-units/", json=payload)
        assert response.status_code == 201
        data = response.json()
        unit_id = data["id"]
        assert data["name"] == "Signal Corps"

        get_response = client.get(f"/api/admin/army-units/{unit_id}")
        assert get_response.status_code == 200
        assert get_response.json()["slug"] == "signal-corps"

    @pytest.mark.api
    def test_update_army_unit_via_api(self, client: TestClient):
        create_response = client.post(
            "/api/admin/army-units/", json={"name": "Medical"}
        )
        assert create_response.status_code == 201
        unit_id = create_response.json()["id"]

        update_response = client.put(
            f"/api/admin/army-units/{unit_id}", json={"name": "Medical Support"}
        )
        assert update_response.status_code == 200
        assert update_response.json()["name"] == "Medical Support"

    @pytest.mark.api
    def test_delete_army_unit_via_api(self, client: TestClient):
        create_response = client.post(
            "/api/admin/army-units/", json={"name": "Field Unit"}
        )
        assert create_response.status_code == 201
        unit_id = create_response.json()["id"]

        delete_response = client.delete(f"/api/admin/army-units/{unit_id}")
        assert delete_response.status_code == 200

        get_response = client.get(f"/api/admin/army-units/{unit_id}")
        assert get_response.status_code == 404
