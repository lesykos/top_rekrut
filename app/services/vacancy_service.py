from typing import Sequence
from sqlmodel import Session
from app.core.exceptions import NotFoundError
from app.api.utils import get_offset_limit_from_range
from app.models.vacancy import (
    Vacancy,
    VacancyCreate,
    VacancyUpdate,
)
from app.repositories import VacancyRepository
from .base import BaseService


class VacancyService(BaseService[Vacancy]):
    """Service for Vacancy business logic."""

    def __init__(self, session: Session):
        super().__init__(session)
        self.repository = VacancyRepository(session)

    def count_vacancies(self, filter_: dict[str, str] | None = None) -> int:
        """Count Vacancies with optional filters."""
        return self.repository.count_all(filter_)

    def get_vacancy(self, vacancy_id: int) -> Vacancy:
        """Get Vacancy by ID"""
        vacancy = self.repository.get_by_id(vacancy_id)
        if vacancy is None:
            raise NotFoundError(f"Vacancy {vacancy_id} not found")
        return vacancy

    def get_vacancies(
        self,
        sort: list[str] | None = None,
        range_: list[int] | None = None,
        filter_: dict[str, str] | None = None,
    ) -> Sequence[Vacancy]:
        """Get a list of Vacancies"""
        offset, limit = get_offset_limit_from_range(range_)
        return self.repository.get_all(sort, filter_, offset, limit)

    # def get_vacancies_public(self) -> VacanciesPublic:
    #     """Get a list of public Vacancies"""
    #     vacancies = self.repository.get_all()
    #     vacancies_public = [
    #         VacancyPublic.model_validate(vacancy) for vacancy in vacancies
    #     ]
    #     return VacanciesPublic(data=vacancies_public, count=len(vacancies_public))

    def create_vacancy(self, vacancy_data: VacancyCreate) -> Vacancy:
        """Create new Vacancy"""
        return self.repository.create_from_data(vacancy_data)

    def update_vacancy(self, vacancy_id: int, vacancy_data: VacancyUpdate) -> Vacancy:
        """Update existing Vacancy"""
        existing_vacancy = self.get_vacancy(vacancy_id)
        return self.repository.update_from_data(existing_vacancy, vacancy_data)

    def delete_vacancy(self, vacancy_id: int) -> None:
        """Delete existing Vacancy"""
        existing_vacancy = self.get_vacancy(vacancy_id)
        self.repository.delete(existing_vacancy)
