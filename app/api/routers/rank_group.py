from fastapi import APIRouter
from app.api.deps import SessionDep
from app.models.rank_group import RankGroupsPublic
from app.services import RankGroupService

router = APIRouter(
    prefix="/rank-groups",
    tags=["rank-groups"],
    responses={404: {"description": "Not found"}},
)


# Get all RankGroupsPublic
@router.get("/", response_model=RankGroupsPublic)
def get_rank_groups(session: SessionDep) -> RankGroupsPublic:
    return RankGroupService(session).get_rank_groups_public()
