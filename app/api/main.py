from fastapi import APIRouter

from .routers import items, utils, army_branch, army_unit, rank_group, vacancy
from .internal import admin

api_router = APIRouter()
api_router.include_router(items.router)
api_router.include_router(utils.router)
api_router.include_router(army_branch.router)
api_router.include_router(army_unit.router)
api_router.include_router(rank_group.router)
api_router.include_router(vacancy.router)
api_router.include_router(admin.admin_router)
