from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, Sequence
from sqlmodel import Session, SQLModel, select

T = TypeVar("T", bound=SQLModel)


class BaseRepository(ABC, Generic[T]):
    """Base repository class with common CRUD operations."""

    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def get_model_class(self) -> type[T]:
        """Return the SQLModel class for this repository."""
        pass

    def get_by_id(self, id: int) -> Optional[T]:
        """Get entity by ID."""
        return self.session.get(self.get_model_class(), id)

    def get_all(self) -> Sequence[T]:
        """Get all entities."""
        return self.session.exec(select(self.get_model_class())).all()

    def create(self, entity: T) -> T:
        """Create new entity."""
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def update(self, entity: T) -> T:
        """Update existing entity."""
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def delete(self, entity: T) -> None:
        """Delete entity."""
        self.session.delete(entity)
        self.session.commit()

    def exists(self, id: int) -> bool:
        """Check if entity exists."""
        return self.get_by_id(id) is not None
