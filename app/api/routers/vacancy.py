from fastapi import APIRouter
from app.api.deps import SessionDep
from app.models.vacancy import VacanciesPublic
from app.services import VacancyService

router = APIRouter(
    prefix="/vacancies",
    tags=["vacancies"],
    responses={404: {"description": "Not found"}},
)


# Get all Vacancies
@router.get("/", response_model=VacanciesPublic)
def get_vacancies(session: SessionDep) -> VacanciesPublic:
    return VacancyService(session).get_vacancies_public()
