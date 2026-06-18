from typing import List, Optional
from app.core.config import INSTITUTE_MASTER_PATH
from app.core.exceptions import EntityNotFoundError
from app.schemas.institute import Institute
from app.repositories.base_repository import BaseRepository

class InstituteRepository(BaseRepository):
    def __init__(self):
        self._institutes = self.load_csv(INSTITUTE_MASTER_PATH, Institute)
        self._id_map = {inst.institute_id: inst for inst in self._institutes}

    def get_all(self) -> List[Institute]:
        return self._institutes

    def get_by_id(self, institute_id: str) -> Optional[Institute]:
        return self._id_map.get(institute_id)

    def get_by_id_strict(self, institute_id: str) -> Institute:
        inst = self.get_by_id(institute_id)
        if not inst:
            raise EntityNotFoundError(f"Institute ID {institute_id} not found.")
        return inst
