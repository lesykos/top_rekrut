from fastapi import APIRouter, Response, Query
from app.api.deps import SessionDep
from app.api.utils import (
    resolve_start_end_from_range,
    decode_and_validate_query_params,
)
from app.models.army_unit import ArmyUnitsPublic
from app.services import ArmyUnitService

router = APIRouter(
    prefix="/army-units",
    tags=["army-units"],
    responses={404: {"description": "Not found"}},
)


# Index - Get all ArmyUnits
@router.get("/", response_model=ArmyUnitsPublic)
def get_army_units(
    session: SessionDep,
    response: Response,
    sort: str | None = Query(None),
    range_param: str | None = Query(None, alias="range"),
    filter_param: str | None = Query(None, alias="filter"),
) -> ArmyUnitsPublic:
    decoded_args = decode_and_validate_query_params(sort, range_param, filter_param)

    army_units = ArmyUnitService(session).get_army_units_public(
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
