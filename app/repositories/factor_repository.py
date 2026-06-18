from typing import List
from app.core.config import FACTOR_MASTER_PATH
from app.schemas.factor import Factor
from app.repositories.base_repository import BaseRepository

class FactorRepository(BaseRepository):
    def __init__(self):
        self._factors = self.load_csv(FACTOR_MASTER_PATH, Factor)
        self._institute_map = {}
        for factor in self._factors:
            self._institute_map.setdefault(factor.institute_id, []).append(factor)

    def get_all(self) -> List[Factor]:
        return self._factors

    def get_by_institute(self, institute_id: str) -> List[Factor]:
        return self._institute_map.get(institute_id, [])
