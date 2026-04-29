from typing import List
from fastapi import APIRouter
from app.api.deps import SessionDep
from app.models.army_branch import ArmyBranch, ArmyBranchCreate, ArmyBranchUpdate
from app.services import ArmyBranchService

router = APIRouter(prefix="/army-branches", tags=["army-branches"])


# Index - show all the army branches
@router.get("/")
async def get_army_branches(session: SessionDep) -> List[ArmyBranch] | None:
    return ArmyBranchService(session).get_army_branches()


# Show - show army branch by slug
@router.get("/{slug}")
async def get_army_branch(slug: str, session: SessionDep) -> ArmyBranch | None:
    return ArmyBranchService(session).get_army_branch_by_slug(slug)


# Create - create new army branch
@router.post("/")
async def create_army_branch(
    army_branch_data: ArmyBranchCreate, session: SessionDep
) -> ArmyBranch | None:
    return ArmyBranchService(session).create_army_branch(army_branch_data)


# Update - update army branch by slug
@router.patch("/{slug}")
async def update_army_branch(
    slug: str, army_branch_data: ArmyBranchUpdate, session: SessionDep
) -> ArmyBranch | None:
    return ArmyBranchService(session).update_army_branch(slug, army_branch_data)


# Delete - delete army branch by slug
@router.delete("/{slug}")
async def delete_army_branch(slug: str, session: SessionDep):
    ArmyBranchService(session).delete_army_branch(slug)
    return {"message": "Army branch deleted successfully!"}
