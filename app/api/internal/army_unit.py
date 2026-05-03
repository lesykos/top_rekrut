from typing import Sequence
from fastapi import APIRouter, Response, Query
from app.api.deps import SessionDep
from app.api.utils import (
    resolve_start_end_from_range,
    decode_and_validate_query_params,
)
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
    decoded_args = decode_and_validate_query_params(sort, range_param, filter_param)

    army_units = ArmyUnitService(session).get_army_units(
        sort=decoded_args["sort_value"],
        range_=decoded_args["range_value"],
        filter_=decoded_args["filter_value"],
    )
    count_army_units = ArmyUnitService(session).count_army_units(
        decoded_args["filter_value"]
    )

    start, end = resolve_start_end_from_range(
        decoded_args["range_value"], count_army_units
    )

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
