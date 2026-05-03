from typing import Sequence
from fastapi import APIRouter, Response, Query
from app.api.deps import SessionDep
from app.api.utils import (
    resolve_start_end_from_range,
    decode_and_validate_query_params,
)
from app.models.rank_group import RankGroup, RankGroupCreate, RankGroupUpdate
from app.services import RankGroupService

router = APIRouter(prefix="/rank-groups", tags=["rank-groups"])


# Index - show all RankGroups
@router.get("/")
def get_rank_groups(
    session: SessionDep,
    response: Response,
    sort: str | None = Query(None),
    range_param: str | None = Query(None, alias="range"),
    filter_param: str | None = Query(None, alias="filter"),
) -> Sequence[RankGroup]:
    decoded_args = decode_and_validate_query_params(sort, range_param, filter_param)

    rank_groups = RankGroupService(session).get_rank_groups(
        sort=decoded_args["sort_value"],
        range_=decoded_args["range_value"],
        filter_=decoded_args["filter_value"],
    )
    count_rank_groups = RankGroupService(session).count_rank_groups(
        decoded_args["filter_value"]
    )

    start, end = resolve_start_end_from_range(
        decoded_args["range_value"], count_rank_groups
    )

    response.headers["Content-Range"] = f"rank-groups {start}-{end}/{count_rank_groups}"
    return rank_groups


# Show - show RankGroup by ID
@router.get("/{rank_group_id}")
def get_rank_group(rank_group_id: int, session: SessionDep) -> RankGroup:
    return RankGroupService(session).get_rank_group(rank_group_id)


# Show - show RankGroup by slug
# @router.get("/{slug}")
# def get_rank_group(slug: str, session: SessionDep) -> RankGroup:
#     return RankGroupService(session).get_rank_group_by_slug(slug)


# Create - create new RankGroup
@router.post("/", status_code=201)
def create_rank_group(
    rank_group_data: RankGroupCreate, session: SessionDep
) -> RankGroup:
    return RankGroupService(session).create_rank_group(rank_group_data)


# Update - update RankGroup by slug
@router.put("/{rank_group_id}")
def update_rank_group(
    rank_group_id: int, rank_group_data: RankGroupUpdate, session: SessionDep
) -> RankGroup:
    return RankGroupService(session).update_rank_group(rank_group_id, rank_group_data)


# Delete - delete RankGroup by slug
@router.delete("/{rank_group_id}")
def delete_rank_group(rank_group_id: int, session: SessionDep):
    RankGroupService(session).delete_rank_group(rank_group_id)
    return {"message": "Rank group deleted successfully!"}
