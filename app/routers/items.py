from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


fake_items_db = {
    "car": {"name": "Toyota Corolla"},
    "motorcycle": {"name": "Honda CB750 Hornet"},
}


@router.get("/")
async def read_items():
    return fake_items_db


@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}
