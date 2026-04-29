from fastapi import APIRouter
from app.api.deps import TokenDep
from . import army_branch

admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={403: {"description": "Forbidden"}},
    dependencies=[TokenDep],
)

admin_router.include_router(army_branch.router)
