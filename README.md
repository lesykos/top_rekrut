# Top Rekrut

## Description

A FastAPI-based backend service for managing vacancies in the Armed Forces of Ukraine (AFU), providing detailed information with army unit, army branch, rank group.

## Features

- The Model-Service-Repository (MSR) pattern to separate data access, business logic, and API routing.
- RESTful API with structured endpoints.
- Retrieve and manage army units, branches, and rank groups.
- Filtering and Pagination: Index routes support filtering, sorting, pagination and returns total counts via Content-Range header.
- Centralized decoding/validation of list query params and consistent pagination across list endpoints.
- Error Handling and Validation with global exception handlers.
- CORS enabled to allow cross-origin requests.
- PostgreSQL database integration with SQLModel ORM.
- Database migration by Alembic.
- **pytest** as the testing framework: Unit Tests, Integration Tests, API Tests.
- Auth0 authentication support.

## Tech Stack

- **Python** - Core programming language
- **FastAPI** - Web framework for building APIs
- **PostgreSQL** - Relational database
- **SQLModel** - ORM based on SQLAlchemy and Pydantic
- **Alembic** - database migration
- **Auth0** - User Authentication

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/lesykos/top_rekrut.git
   cd top_rekrut
   ```

2. Use a virtual environment:
   ```bash
   python -m venv .venv
   ./.venv/Scripts/activate 
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (see Environment Variables section).

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

## Running the Project

Start the development server:
```bash
fastapi dev
```

The API will be available at `http://localhost:8000`.

## Environment Variables

Create a `.env` file in the root directory from the template `.env.example`

## Main resources
- Army Unit: `army-units`
- Army branch: `army-branches`
- Rank group: `rank-groups`

## API Endpoints

Base URL: `http://localhost:8000/api`

- `GET /admin/army-units` - Retrieve list of Army Units
- `POST /admin/army-units` - Create Army Unit
- `GET /admin/army-units/{id}` - Get Army Unit by ID
- `PUT /admin/army-units/{id}` - Update Army Unit
- `DELETE /admin/army-units` - Delete Army Unit
- `GET /admin/army-units?sort=["created_at","ASC"]&range=[0, 4]&filter={"name":"414"}` - Filtering, sorting, pagination.


### Same routes and logic for `army-branches` and `rank-groups`

## Example Request

Retrieve army branches:
```bash
curl -X GET "http://localhost:8000/api/admin/army-units" \
     -H "accept: application/json"
```
