# By adding this we can import directly from the folder level:
# from app.services import VacancyRepository

from .base import BaseService
from .army_branch_service import ArmyBranchService
from .army_unit_service import ArmyUnitService
from .rank_group_service import RankGroupService
from .vacancy_service import VacancyService

__all__ = [
    "ArmyBranchService",
    "ArmyUnitService",
    "BaseService",
    "RankGroupService",
    "VacancyService",
]
