from fastapi import APIRouter, Response, Query
from app.api.deps import SessionDep
from app.api.utils import (
    resolve_start_end_from_range,
    decode_and_validate_query_params,
)
from app.models.vacancy import VacanciesPublic
from app.services import VacancyService

router = APIRouter(
    prefix="/vacancies",
    tags=["vacancies"],
    responses={404: {"description": "Not found"}},
)


# Index - Get all Vacancies
@router.get("/", response_model=VacanciesPublic)
def get_vacancies(
    session: SessionDep,
    response: Response,
    sort: str | None = Query(None),
    range_param: str | None = Query(None, alias="range"),
    filter_param: str | None = Query(None, alias="filter"),
) -> VacanciesPublic:
    decoded_args = decode_and_validate_query_params(sort, range_param, filter_param)

    vacancies = VacancyService(session).get_vacancies_public(
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
