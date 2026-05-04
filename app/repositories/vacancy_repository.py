from typing import Sequence
from sqlmodel import select, col, func
from sqlalchemy.exc import IntegrityError
from app.core.exceptions import ConflictError
from app.models.vacancy import Vacancy, VacancyCreate, VacancyUpdate
from .base import BaseRepository

# from sqlalchemy.orm import joinedload


class VacancyRepository(BaseRepository[Vacancy]):

    def get_model_class(self) -> type[Vacancy]:
        return Vacancy

    def count_all(self, filters: dict[str, str] | None = None) -> int:
        """Count all Vacancies with optional filters."""
        query = select(func.count()).select_from(Vacancy)
        query = self.admin_query_filters(query, filters)
        return self.session.exec(query).one()

    def get_all(
        self,
        sort: list[str] | None = None,
        filters: dict[str, str] | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> Sequence[Vacancy]:
        """Get all Vacancies"""
        query = select(Vacancy)
        query = self.admin_query_filters(query, filters)
        query = self.admin_query_sort(query, sort)

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        return self.session.exec(query).all()

    def create_from_data(self, vacancy_data: VacancyCreate) -> Vacancy:
        """Create Vacancy from VacancyCreate data"""
        try:
            vacancy = Vacancy(**vacancy_data.model_dump())
            return self.create(vacancy)
        except IntegrityError as e:
            self.session.rollback()
            raise ConflictError("Database integrity error") from e

    def update_from_data(
        self, vacancy: Vacancy, vacancy_data: VacancyUpdate
    ) -> Vacancy:
        """Update Vacancy from VacancyUpdate data"""
        try:
            update_data = vacancy_data.model_dump(exclude_unset=True, exclude_none=True)
            vacancy.sqlmodel_update(update_data)
            return self.update(vacancy)
        except IntegrityError as e:
            self.session.rollback()
            raise ConflictError("Database integrity error") from e

    def admin_query_filters(self, query, filters):
        if filters:
            for ids in ["id, army_unit_id", "rank_group_id"]:
                if ids in filters:
                    column = getattr(Vacancy, ids)
                    query = query.where(col(column).in_(filters["id"]))
            if "name" in filters:
                query = query.where(col(Vacancy.name).ilike(f'%{filters["name"]}%'))
            if "service_type" in filters:
                query = query.where(Vacancy.service_type == filters["service_type"])
        return query

    def admin_query_sort(self, query, sort):
        if sort:
            sort_field, sort_direction = sort
            column = getattr(Vacancy, sort_field)
            query = query.order_by(
                col(column).asc()
                if sort_direction.upper() == "ASC"
                else col(column).desc()
            )
        else:
            query = query.order_by(col(Vacancy.id).asc())

        return query
