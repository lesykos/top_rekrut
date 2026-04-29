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
@router.get("/")
def get_army_branches(session: SessionDep) -> ArmyBranchesPublic | None:
    return ArmyBranchService(session).get_army_branches_public()
