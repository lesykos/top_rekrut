import json
from typing import Sequence
from fastapi import APIRouter, Response, Query
from app.api.deps import SessionDep
from app.api.utils import resolve_start_end_from_range
from app.core.exceptions import BadRequestError
from app.models.army_unit import ArmyUnit, ArmyUnitCreate, ArmyUnitUpdate
from app.services import ArmyUnitService

router = APIRouter(prefix="/army-units", tags=["army-units"])


# Index - show all ArmyUnits
@router.get("/")
def get_army_units(
    session: SessionDep,
    response: Response,
    sort: str | None = Query(None),
    range_param: str | None = Query(None, alias="range"),
    filter_param: str | None = Query(None, alias="filter"),
) -> Sequence[ArmyUnit]:
    try:
        sort_value = json.loads(sort) if sort else ["id", "DESC"]
        filter_value = json.loads(filter_param) if filter_param else {}
        range_value = json.loads(range_param) if range_param else None
    except json.JSONDecodeError as exc:
        raise BadRequestError(f"Invalid query JSON: {exc.msg}") from None

    army_units = ArmyUnitService(session).get_army_units(
        sort=sort_value, range_=range_value, filter_=filter_value
    )
    count_army_units = ArmyUnitService(session).count_army_units(filter_=filter_value)

    start, end = resolve_start_end_from_range(range_value, count_army_units)

    response.headers["Content-Range"] = f"army-units {start}-{end}/{count_army_units}"
    return army_units


# Show - show ArmyUnit ID
@router.get("/{army_unit_id}")
def get_army_unit(army_unit_id: int, session: SessionDep) -> ArmyUnit:
    return ArmyUnitService(session).get_army_unit(army_unit_id)


# Show - show ArmyUnit by slug
# @router.get("/{slug}")
# def get_army_unit(slug: str, session: SessionDep) -> ArmyUnit:
#     return ArmyUnitService(session).get_army_unit_by_slug(slug)


# Create - create new ArmyUnit
@router.post("/", status_code=201)
def create_army_unit(army_unit_data: ArmyUnitCreate, session: SessionDep) -> ArmyUnit:
    return ArmyUnitService(session).create_army_unit(army_unit_data)


# Update - update ArmyUnit
@router.put("/{army_unit_id}")
def update_army_unit(
    army_unit_id: int, army_unit_data: ArmyUnitUpdate, session: SessionDep
) -> ArmyUnit:
    return ArmyUnitService(session).update_army_unit(army_unit_id, army_unit_data)


# Delete - delete ArmyUnit by army_unit_id
@router.delete("/{army_unit_id}")
def delete_army_unit(army_unit_id: int, session: SessionDep):
    ArmyUnitService(session).delete_army_unit(army_unit_id)
    return {"message": "Army unit deleted successfully!"}
