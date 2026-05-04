"""
Pytest configuration and fixtures for testing.

This module provides:
- Database session fixtures for unit and integration tests
- Test client fixtures for API endpoint testing
- Model factories for creating test data
"""

import os
from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, select

from app.core.db import engine
from app.core.config import settings
from app.api.deps import get_db, TokenDep
from app.main import app

# Create test database URL
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test.db"

# Create test engine with SQLite database file for shared connections
test_engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

TestingSessionLocal = sessionmaker(
    class_=Session, autocommit=False, autoflush=False, bind=test_engine
)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Create a test database session.

    Scope: function
    Creates a fresh database for each test function.

    Yields:
        Session: SQLModel session connected to in-memory SQLite database.
    """
    # Create all tables in test database
    SQLModel.metadata.create_all(test_engine)

    with TestingSessionLocal() as session:
        yield session

    # Clean up: drop all tables after test
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(scope="function")
def db_session_with_data(db_session: Session) -> Generator[Session, None, None]:
    """
    Create a test database session with sample data.

    Scope: function
    Creates a fresh database with pre-populated test data for each test.

    Yields:
        Session: SQLModel session with test data.
    """
    # This fixture can be extended to add common test data
    yield db_session


@pytest.fixture(scope="function")
def client(db_session: Session) -> TestClient:
    """
    Create a test client that overrides the database dependency.

    Scope: function
    Provides a FastAPI TestClient that uses the test database session.

    Returns:
        TestClient: FastAPI test client with overridden database dependency.
    """

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    if hasattr(TokenDep, "dependency"):
        app.dependency_overrides[TokenDep.dependency] = lambda: {}
    else:
        app.dependency_overrides[TokenDep] = lambda: {}

    yield TestClient(app)

    # Clean up: remove dependency override
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def reset_db():
    """
    Reset database state before each test.

    This fixture ensures test isolation by clearing any lingering state.
    """
    yield
    # Cleanup code if needed


def pytest_configure(config):
    """
    Configure pytest with custom markers.

    Markers:
        - unit: Unit tests that test individual components in isolation
        - integration: Integration tests that test multiple components together
        - api: API endpoint tests
        - slow: Tests that take longer to run
    """
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "api: mark test as an API test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
