# Top Rekrut

## Description

A FastAPI-based backend service for managing vacancies in the Armed Forces of Ukraine (AFU), providing detailed information with army unit, army branch, rank group.

## Features

- RESTful API with structured endpoints.
- The Model-Service-Repository (MSR) pattern to separate data access, business logic, and API routing.
- Publicly accessible routes and restricted Admin-only endpoints.
- Retrieve and manage vacancies, army units, branches, and rank groups.
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

## Project Structure

The project is organized into the following main directories:
```
├── app
│   ├── main.py         # application entrypoint
│   ├── alembic         # migration scripts
│   ├── api             # router
│   │   ├── routers     # public API route definitions
│   │   └── internal    # admin endpoints and protected routes.
│   ├── core            # configuration, database setup
│   ├── models          # SQLModel data models, validation, and schemas
│   ├── repositories    # DB access layer for CRUD operations
│   └── services        # business logic layer that orchestrates repositories and model operations
├── tests               # tests
```

Each section separates concerns so the API, database models, business logic, and repository access are easy to maintain and extend.

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
- Vacancy: `vacancies`
- Army Unit: `army-units`
- Army branch: `army-branches`
- Rank group: `rank-groups`

## API Endpoints

Base URL: `http://localhost:8000/api`

### Public Routes

No authentication required. Used for fetching public data.

- `GET /vacancies` - Get a list of vacancies
- `GET /army-units` - Get a list of army units
- `GET /army-branches` - Get a list of army branches
- `GET /rank-groups` - Get a list of rank groups

### Admin Routes
Requires `Authorization: Bearer <admin_token>`.
- `GET /admin/vacancies` - Retrieve list of Vacancies
- `POST /admin/vacancies` - Create Vacancy
- `GET /admin/vacancies/{id}` - Get Vacancy by ID
- `PUT /admin/vacancies/{id}` - Update Vacancy
- `DELETE /admin/vacancies` - Delete Vacancy
- `GET /admin/vacancies?sort=["created_at","ASC"]&range=[0, 4]&filter={"name":"414"}` - Filtering, sorting, pagination.


### Same routes and logic for `army-units`, `army-branches` and `rank-groups`.

