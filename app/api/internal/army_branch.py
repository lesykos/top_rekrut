from typing import Sequence
from fastapi import APIRouter, Response
from app.api.deps import SessionDep
from app.models.army_branch import ArmyBranch, ArmyBranchCreate, ArmyBranchUpdate
from app.services import ArmyBranchService

router = APIRouter(prefix="/army-branches", tags=["army-branches"])


# Index - show all the army branches
@router.get("/")
def get_army_branches(session: SessionDep, response: Response) -> Sequence[ArmyBranch]:
    army_branches = ArmyBranchService(session).get_army_branches()
    army_branches_count = len(army_branches)
    response.headers["Content-Range"] = (
        f"army-branches 0-{army_branches_count}/{army_branches_count}"
    )
    return army_branches


# Show - show army branch by ID
@router.get("/{id}")
def get_army_branch_by_id(id: int, session: SessionDep) -> ArmyBranch:
    return ArmyBranchService(session).get_army_branch(id)


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
@router.put("/{id}", status_code=201)
def update_army_branch_by_id(
    id: int, army_branch_data: ArmyBranchUpdate, session: SessionDep
) -> ArmyBranch:
    return ArmyBranchService(session).update_army_branch(id, army_branch_data)


# @router.patch("/{slug}")
# def update_army_branch_by_slug(
#     slug: str, army_branch_data: ArmyBranchUpdate, session: SessionDep
# ) -> ArmyBranch:
#     return ArmyBranchService(session).update_army_branch_by_slug(slug, army_branch_data)


# Delete - delete army branch
@router.delete("/{id}")
def delete_army_branch(id: int, session: SessionDep):
    ArmyBranchService(session).delete_army_branch(id)
    return {"message": "Army branch deleted successfully!"}
