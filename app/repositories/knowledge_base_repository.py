from typing import List, Optional
from app.core.config import KNOWLEDGE_BASE_PATH
from app.schemas.knowledge import KnowledgeBaseEntry
from app.repositories.base_repository import BaseRepository

class KnowledgeBaseRepository(BaseRepository):
    def __init__(self):
        self._entries = self.load_json(KNOWLEDGE_BASE_PATH, KnowledgeBaseEntry)
        self._id_map = {entry.institute_id: entry for entry in self._entries}

    def get_all(self) -> List[KnowledgeBaseEntry]:
        return self._entries

    def get_knowledge(self, institute_id: str) -> Optional[KnowledgeBaseEntry]:
        return self._id_map.get(institute_id)
