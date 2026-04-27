from typing import List, Optional
from sqlmodel import select
from app.models.item import Item
from .base import BaseRepository


class ItemRepository(BaseRepository[Item]):
    """Repository for Item entity operations."""

    def get_model_class(self) -> type[Item]:
        return Item

    def get_by_name(self, name: str) -> Optional[Item]:
        """Get item by name."""
        return self.session.exec(select(Item).where(Item.name == name)).first()
