from typing import Sequence
from fastapi import APIRouter, Response, Query
from app.api.deps import SessionDep
from app.api.utils import (
    resolve_start_end_from_range,
    decode_and_validate_query_params,
)
from app.models.vacancy import Vacancy, VacancyCreate, VacancyUpdate
from app.services import VacancyService

router = APIRouter(prefix="/vacancies", tags=["vacancies"])


# Index - show all Vacancies
@router.get("/")
def get_vacancies(
    session: SessionDep,
    response: Response,
    sort: str | None = Query(None),
    range_param: str | None = Query(None, alias="range"),
    filter_param: str | None = Query(None, alias="filter"),
) -> Sequence[Vacancy]:
    decoded_args = decode_and_validate_query_params(sort, range_param, filter_param)

    vacancies = VacancyService(session).get_vacancies(
        sort=decoded_args["sort_value"],
        range_=decoded_args["range_value"],
        filter_=decoded_args["filter_value"],
    )
    count_vacancies = VacancyService(session).count_vacancies(
        decoded_args["filter_value"]
    )

    start, end = resolve_start_end_from_range(
        decoded_args["range_value"], count_vacancies
    )

    response.headers["Content-Range"] = f"vacancies {start}-{end}/{count_vacancies}"
    return vacancies


# Show - show Vacancy ID
@router.get("/{vacancy_id}")
def get_vacancy(vacancy_id: int, session: SessionDep) -> Vacancy:
    return VacancyService(session).get_vacancy(vacancy_id)


# Create - create new Vacancy
@router.post("/")
def create_vacancy(vacancy_data: VacancyCreate, session: SessionDep) -> Vacancy:
    return VacancyService(session).create_vacancy(vacancy_data)


# Update - update Vacancy
@router.put("/{vacancy_id}")
def update_vacancy(
    vacancy_id: int, vacancy_data: VacancyUpdate, session: SessionDep
) -> Vacancy:
    return VacancyService(session).update_vacancy(vacancy_id, vacancy_data)


# Delete - delete Vacancy by vacancy_id
@router.delete("/{vacancy_id}")
def delete_vacancy(vacancy_id: int, session: SessionDep):
    VacancyService(session).delete_vacancy(vacancy_id)
    return {"message": "Vacancy deleted successfully!"}
