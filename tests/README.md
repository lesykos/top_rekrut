# Testing Documentation

This document provides comprehensive information about the testing setup for the TopRekrut Backend project.

## Overview

The project uses **pytest** as the testing framework with comprehensive coverage reporting. Tests are organized into:
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test interactions between components
- **API Tests**: Test HTTP endpoints

## Test Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── test_models.py           # Unit tests for models
├── test_repositories.py     # CRUD operation tests
├── test_services.py         # Business logic tests
├── test_api.py              # API endpoint tests
└── test_integration.py      # Integration tests
```

## Installation

All testing dependencies are included in `requirements.txt`:

```bash
pip install -r requirements.txt
```

Key testing packages:
- `pytest==8.3.3` - Testing framework
- `pytest-cov==6.0.0` - Coverage reporting
- `pytest-asyncio==0.24.0` - Async test support
- `pytest-xdist==3.7.0` - Parallel test execution
- `factory-boy==3.3.1` - Test data factories (optional)

## Running Tests

### Run All Tests
```bash
pytest app/main.py
```

### Run Specific Test File
```bash
pytest tests/test_models.py
pytest tests/test_repositories.py
pytest tests/test_services.py
pytest tests/test_api.py
pytest tests/test_integration.py
```

### Run Tests by Marker
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only API tests
pytest -m api

# Exclude slow tests
pytest -m "not slow"
```

### Run Tests in Parallel
```bash
pytest -n auto  # Automatically uses all available CPUs
pytest -n 4     # Use 4 workers
```

### Run with Verbose Output
```bash
pytest -v
```

### Run Tests with Debug Output
```bash
pytest -vv -s  # -s shows print statements
```

## Coverage Reporting

### Generate Coverage Report
```bash
# Terminal report
pytest --cov=app --cov-report=term-missing

# HTML report
pytest --cov=app --cov-report=html

# XML report (for CI/CD)
pytest --cov=app --cov-report=xml

# All formats (configured in pytest.ini)
pytest
```

The pytest.ini is configured to:
- Generate HTML coverage report in `htmlcov/index.html`
- Display term-missing report in terminal
- Generate XML report for CI/CD integration
- Fail if coverage drops below 50%

### View HTML Coverage Report
After running tests:
```bash
# Windows
start htmlcov/index.html

# macOS
open htmlcov/index.html

# Linux
xdg-open htmlcov/index.html
```

## Test Coverage Goals

**Target: >50% code coverage**

Current coverage by module (aim for):
- `models/` - 95%+ (validation logic)
- `repositories/` - 90%+ (CRUD operations)
- `services/` - 85%+ (business logic)
- `api/` - 85%+ (endpoints)
- `core/` - 90%+ (configuration, exceptions)

## Test Types

### Unit Tests (`test_models.py`)
Test individual models and their validation:
- Field validation (min/max length, ranges)
- Default values
- Schema conversion
- Model relationships

Example:
```python
@pytest.mark.unit
def test_item_name_max_length_validation(self):
    """Test Item name maximum length validation."""
    with pytest.raises(Exception):
        ItemBase(name="x" * 256)
```

### Repository Tests (`test_repositories.py`)
Test CRUD operations at the data access layer:
- Create entities
- Read by ID, name, slug
- Update entities
- Delete entities
- Check existence
- Get all entities

Example:
```python
@pytest.mark.unit
def test_create_item(self, db_session: Session):
    """Test creating an item via repository."""
    repo = ItemRepository(db_session)
    item = Item(name="Test Item")
    created_item = repo.create(item)
    assert created_item.id is not None
```

### Service Tests (`test_services.py`)
Test business logic and error handling:
- Create/read/update/delete operations
- Exception handling
- Data validation
- Business rules

Example:
```python
@pytest.mark.unit
def test_get_item_not_found(self, db_session: Session):
    """Test retrieving a non-existent item raises HTTPException."""
    service = ItemService(db_session)
    with pytest.raises(HTTPException) as exc_info:
        service.get_item(999)
    assert exc_info.value.status_code == 404
```

### API Tests (`test_api.py`)
Test HTTP endpoints and responses:
- Status codes (200, 201, 404, 409, etc.)
- Response structure
- Error handling
- Data serialization

Example:
```python
@pytest.mark.api
def test_read_items_empty(self, client: TestClient):
    """Test reading items when none exist."""
    response = client.get("/api/items/")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
```

### Integration Tests (`test_integration.py`)
Test complete workflows across layers:
- Full CRUD lifecycle
- Cross-entity operations
- Database transactions
- API to database flow

Example:
```python
@pytest.mark.integration
def test_item_full_lifecycle(self, db_session: Session):
    """Test complete item lifecycle: create, read, update, delete."""
    service = ItemService(db_session)
    
    # Create
    created = service.create_item(ItemCreate(name="Test"))
    # Read
    retrieved = service.get_item(created.id)
    # Update
    updated = service.update_item(created.id, ItemUpdate(name="Updated"))
    # Delete
    service.delete_item(created.id)
```

## Fixtures

### Database Fixtures

**`db_session`** - Function-scoped fixture
- Fresh SQLite in-memory database for each test
- Automatically creates and drops all tables
- Ensures test isolation

```python
def test_something(db_session: Session):
    """Each test gets a clean database."""
    item = Item(name="Test")
    db_session.add(item)
    db_session.commit()
```

**`db_session_with_data`** - Pre-populated database
- Extends `db_session` with sample data
- Use when tests need initial data

### Client Fixtures

**`client`** - FastAPI TestClient
- Overrides database dependency
- Uses test database session
- Provides HTTP test interface

```python
def test_api(client: TestClient):
    """Test HTTP endpoints."""
    response = client.get("/api/items/")
    assert response.status_code == 200
```

## Writing New Tests

### Template for Unit Test
```python
@pytest.mark.unit
def test_specific_behavior(self, db_session: Session):
    """Test description."""
    # Arrange
    repo = ItemRepository(db_session)
    item = Item(name="Test")
    
    # Act
    result = repo.create(item)
    
    # Assert
    assert result.id is not None
```

### Template for API Test
```python
@pytest.mark.api
def test_endpoint_behavior(self, client: TestClient):
    """Test endpoint description."""
    # Arrange
    payload = {"name": "Test"}
    
    # Act
    response = client.post("/api/items/", json=payload)
    
    # Assert
    assert response.status_code == 201
    assert response.json()["name"] == "Test"
```

### Template for Integration Test
```python
@pytest.mark.integration
def test_full_workflow(self, db_session: Session):
    """Test complete workflow."""
    service = ItemService(db_session)
    
    # Create
    item = service.create_item(ItemCreate(name="Test"))
    
    # Use
    retrieved = service.get_item(item.id)
    
    # Cleanup
    service.delete_item(item.id)
```

## Best Practices

1. **Arrange-Act-Assert**: Follow AAA pattern
   ```python
   # Arrange - Set up test data
   item = Item(name="Test")
   db_session.add(item)
   db_session.commit()
   
   # Act - Perform the action
   result = service.get_item(item.id)
   
   # Assert - Verify the result
   assert result.name == "Test"
   ```

2. **Test One Thing**: Each test should test a single behavior
   - Don't combine multiple assertions into one test
   - If behavior needs multiple assertions, group related ones

3. **Descriptive Names**: Test name should describe what is tested
   ```python
   # Good
   def test_item_name_max_length_validation_fails()
   
   # Bad
   def test_validation()
   ```

4. **Use Fixtures**: Share common setup via fixtures
   ```python
   @pytest.fixture
   def sample_item(db_session):
       return Item(name="Sample")
   
   def test_something(sample_item):
       assert sample_item.name == "Sample"
   ```

5. **Mark Tests Appropriately**: Use markers for categorization
   ```python
   @pytest.mark.unit
   @pytest.mark.slow
   def test_expensive_operation()
   ```

6. **Test Edge Cases**: Don't just test happy paths
   ```python
   def test_invalid_input()
   def test_empty_list()
   def test_boundary_values()
   def test_null_handling()
   ```

7. **Mock External Dependencies**: Keep tests isolated
   - Use in-memory database (already done via fixtures)
   - Mock external APIs if needed
   - Don't test external services

## Continuous Integration

The test suite is designed for CI/CD pipelines:

### GitHub Actions Example
```yaml
- name: Run tests
  run: |
    pytest --cov=app --cov-report=xml
    
- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
    flags: unittests
    fail_ci_if_error: true
```

## Troubleshooting

### Tests Fail with "Database is locked"
- Ensure only one test worker is using the database
- Use `pytest -n 1` to run sequentially
- Check for leftover processes

### Import Errors in Tests
- Verify `PYTHONPATH` includes project root
- Run tests from project root: `pytest`
- Check virtual environment is activated

### Fixture Not Found
- Ensure fixtures are in `conftest.py` or same file
- Check fixture is properly decorated: `@pytest.fixture`
- Verify fixture name matches parameter name

### Coverage Below 50%
- Identify uncovered lines: `--cov-report=term-missing`
- Add tests for missing lines
- Use `# pragma: no cover` for lines that can't be tested

### Async Test Issues
- Ensure `pytest-asyncio` is installed
- Use `@pytest.mark.asyncio` decorator
- Use `async def test_*()` for async tests

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Coverage Plugin](https://pytest-cov.readthedocs.io/)
- [FastAPI Testing](https://fastapi.tiangolo.com/advanced/testing/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Testing Best Practices](https://docs.pytest.org/en/stable/goodpractices.html)

## Contact

For questions about testing setup, contact the development team.
