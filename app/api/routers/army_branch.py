# from typing import List
from fastapi import APIRouter
from app.api.deps import SessionDep
from app.models.army_branch import ArmyBranchesPublic
from app.services import ArmyBranchService

router = APIRouter(
    prefix="/army-branches",
    tags=["army-branches"],
    responses={404: {"description": "Not found"}},
)


# Get all ArmyBranchesPublic
# response_model - API correctness
#   (FastAPI will validate the response, filter fields, serialize data)
# return type - developer correctness
#   static typing, readability, catching bugs
@router.get("/", response_model=ArmyBranchesPublic)
def get_army_branches(session: SessionDep) -> ArmyBranchesPublic:
    return ArmyBranchService(session).get_army_branches_public()
