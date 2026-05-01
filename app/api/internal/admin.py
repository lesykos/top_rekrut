from fastapi import APIRouter
from app.api.deps import TokenDep
from . import army_branch, army_unit, rank_group

admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={403: {"description": "Forbidden"}},
    dependencies=[TokenDep],
)

admin_router.include_router(army_branch.router)
admin_router.include_router(army_unit.router)
admin_router.include_router(rank_group.router)
