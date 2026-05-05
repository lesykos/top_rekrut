# By adding this we can import directly from the folder level:
# from app.repositories import VacancyRepository

from .base import BaseRepository
from .army_branch_repository import ArmyBranchRepository
from .army_unit_repository import ArmyUnitRepository
from .rank_group_repository import RankGroupRepository
from .vacancy_repository import VacancyRepository

__all__ = [
    "ArmyBranchRepository",
    "ArmyUnitRepository",
    "BaseRepository",
    "RankGroupRepository",
    "VacancyRepository",
]
