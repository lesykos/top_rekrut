# from typing import List
from fastapi import APIRouter
from app.api.deps import SessionDep
from app.models.army_unit import ArmyUnitsPublic
from app.services import ArmyUnitService

router = APIRouter(
    prefix="/army-units",
    tags=["army-units"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=ArmyUnitsPublic)
def get_army_units(session: SessionDep) -> ArmyUnitsPublic:
    return ArmyUnitService(session).get_army_units_public()
