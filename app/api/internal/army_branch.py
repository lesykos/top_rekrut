import json
from typing import Sequence
from fastapi import APIRouter, Response, Query
from app.api.deps import SessionDep
from app.core.exceptions import BadRequestError
from app.models.army_branch import ArmyBranch, ArmyBranchCreate, ArmyBranchUpdate
from app.services import ArmyBranchService
from ..utils import resolve_start_end_from_range

router = APIRouter(prefix="/army-branches", tags=["army-branches"])


# Index - show all ArmyBranch
@router.get("/")
def get_army_branches(
    session: SessionDep,
    response: Response,
    sort: str | None = Query(None),
    range_param: str | None = Query(None, alias="range"),
    filter_param: str | None = Query(None, alias="filter"),
) -> Sequence[ArmyBranch]:
    try:
        sort_value = json.loads(sort) if sort else ["position", "ASC"]
        filter_value = json.loads(filter_param) if filter_param else {}
        range_value = json.loads(range_param) if range_param else None
    except json.JSONDecodeError as exc:
        raise BadRequestError(f"Invalid query JSON: {exc.msg}") from None

    army_branches = ArmyBranchService(session).get_army_branches(
        sort=sort_value, range_=range_value, filter_=filter_value
    )
    count_army_branches = ArmyBranchService(session).count_army_branches(
        filter_=filter_value
    )

    start, end = resolve_start_end_from_range(range_value, count_army_branches)

    response.headers["Content-Range"] = (
        f"army-branches {start}-{end}/{count_army_branches}"
    )
    return army_branches


# Show - show army branch by ID
@router.get("/{army_branch_id}")
def get_army_branch_by_id(army_branch_id: int, session: SessionDep) -> ArmyBranch:
    return ArmyBranchService(session).get_army_branch(army_branch_id)


# Show - show army branch by slug
# @router.get("/{slug}")
# def get_army_branch_by_slug(slug: str, session: SessionDep) -> ArmyBranch:
#     return ArmyBranchService(session).get_army_branch_by_slug(slug)


# Create - create new army branch
@router.post("/", status_code=201)
def create_army_branch(
    army_branch_data: ArmyBranchCreate, session: SessionDep
) -> ArmyBranch:
    return ArmyBranchService(session).create_army_branch(army_branch_data)


# Update - update army branch by id
@router.put("/{army_branch_id}", status_code=201)
def update_army_branch_by_id(
    army_branch_id: int, army_branch_data: ArmyBranchUpdate, session: SessionDep
) -> ArmyBranch:
    return ArmyBranchService(session).update_army_branch(
        army_branch_id, army_branch_data
    )


# Delete - delete army branch
@router.delete("/{army_branch_id}")
def delete_army_branch(army_branch_id: int, session: SessionDep):
    ArmyBranchService(session).delete_army_branch(army_branch_id)
    return {"message": "Army branch deleted successfully!"}
