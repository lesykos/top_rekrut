from typing import Any
from fastapi import HTTPException
from sqlmodel import Session
from app.models.item import Item, ItemPublic, ItemsPublic
from app.repositories import ItemRepository
from .base import BaseService


class ItemService(BaseService[Item]):
    """Service for item business logic."""

    def __init__(self, session: Session):
        super().__init__(session)
        self.repository = ItemRepository(session)

    def get_item(self, item_id: int) -> Any:
        """Get item by ID with business logic."""
        try:
            item = self.repository.get_by_id(item_id)
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            return ItemPublic.model_validate(item)
        except Exception as e:
            self._handle_exception(e, f"get_item({item_id})")

    def get_items(self) -> Any:
        """Get paginated list of items."""
        try:
            items = self.repository.get_all()
            items_public = [ItemPublic.model_validate(item) for item in items]
            return ItemsPublic(data=items_public, count=len(items_public))
        except Exception as e:
            self._handle_exception(e, "get_items")
