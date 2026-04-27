from typing import Any
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.api.deps import SessionDep
from app.models.item import Item, ItemPublic, ItemsPublic

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=ItemsPublic)
async def read_items(session: SessionDep) -> Any:
    items = session.exec(select(Item)).all()
    return {"data": items, "count": len(items)}


@router.get("/{item_id}", response_model=ItemPublic)
async def read_item(session: SessionDep, item_id: int) -> Any:
    # item = session.exec(select(Item).where(Item.id == item_id)).first()
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
