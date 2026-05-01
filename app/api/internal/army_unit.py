from typing import Sequence
from fastapi import APIRouter
from app.api.deps import SessionDep
from app.models.army_unit import ArmyUnit, ArmyUnitCreate, ArmyUnitUpdate
from app.services import ArmyUnitService

router = APIRouter(prefix="/army-units", tags=["army-units"])


# Index - show all ArmyUnits
@router.get("/")
def get_army_units(session: SessionDep) -> Sequence[ArmyUnit]:
    return ArmyUnitService(session).get_army_units()


# Show - show ArmyUnit by slug
@router.get("/{slug}")
def get_army_unit(slug: str, session: SessionDep) -> ArmyUnit:
    return ArmyUnitService(session).get_army_unit_by_slug(slug)


# Create - create new ArmyUnit
@router.post("/")
def create_army_unit(army_unit_data: ArmyUnitCreate, session: SessionDep) -> ArmyUnit:
    return ArmyUnitService(session).create_army_unit(army_unit_data)


# Update - update ArmyUnit by slug
@router.patch("/{slug}")
def update_army_unit(
    slug: str, army_unit_data: ArmyUnitUpdate, session: SessionDep
) -> ArmyUnit:
    return ArmyUnitService(session).update_army_unit(slug, army_unit_data)


# Delete - delete ArmyUnit by slug
@router.delete("/{slug}")
def delete_army_unit(slug: str, session: SessionDep):
    ArmyUnitService(session).delete_army_unit(slug)
    return {"message": "Army unit deleted successfully!"}
