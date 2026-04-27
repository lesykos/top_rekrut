from typing import Any
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.api.deps import SessionDep, TokenDep
from app.models.item import Item, ItemPublic, ItemsPublic
from app.services import ItemService

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=ItemsPublic)
async def read_items(session: SessionDep) -> Any:
    return ItemService(session).get_items()


@router.get("/{item_id}", dependencies=[TokenDep], response_model=ItemPublic)
async def read_item(session: SessionDep, item_id: int) -> Any:
    return ItemService(session).get_item(item_id)
