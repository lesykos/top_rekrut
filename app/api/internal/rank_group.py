from typing import Sequence
from fastapi import APIRouter
from app.api.deps import SessionDep
from app.models.rank_group import RankGroup, RankGroupCreate, RankGroupUpdate
from app.services import RankGroupService

router = APIRouter(prefix="/rank-groups", tags=["rank-groups"])


# Index - show all RankGroups
@router.get("/")
def get_rank_groups(session: SessionDep) -> Sequence[RankGroup]:
    return RankGroupService(session).get_rank_groups()


# Show - show RankGroup by slug
@router.get("/{slug}")
def get_rank_group(slug: str, session: SessionDep) -> RankGroup:
    return RankGroupService(session).get_rank_group_by_slug(slug)


# Create - create new RankGroup
@router.post("/")
def create_rank_group(
    rank_group_data: RankGroupCreate, session: SessionDep
) -> RankGroup:
    return RankGroupService(session).create_rank_group(rank_group_data)


# Update - update RankGroup by slug
@router.patch("/{slug}")
def update_rank_group(
    slug: str, rank_group_data: RankGroupUpdate, session: SessionDep
) -> RankGroup:
    return RankGroupService(session).update_rank_group(slug, rank_group_data)


# Delete - delete RankGroup by slug
@router.delete("/{slug}")
def delete_rank_group(slug: str, session: SessionDep):
    RankGroupService(session).delete_rank_group(slug)
    return {"message": "Rank group deleted successfully!"}
