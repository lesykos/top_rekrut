from abc import ABC
from typing import Generic, TypeVar
from sqlmodel import Session

T = TypeVar("T")


class BaseService(ABC, Generic[T]):
    """Base service class with common functionality."""

    def __init__(self, session: Session):
        self.session = session

    def _handle_exception(self, e: Exception, operation: str):
        """Handle and log service exceptions."""
        print(f"Error in {operation}: {str(e)}")
        raise e
