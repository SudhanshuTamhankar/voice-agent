from typing import List
from app.core.config import PROFILE_SCORING_ENGINE_PATH
from app.schemas.rule import ScoringRule
from app.repositories.base_repository import BaseRepository

class ScoringRuleRepository(BaseRepository):
    def __init__(self):
        self._rules = self.load_csv(PROFILE_SCORING_ENGINE_PATH, ScoringRule)
        self._institute_map = {}
        for rule in self._rules:
            self._institute_map.setdefault(rule.institute_id, []).append(rule)

    def get_all(self) -> List[ScoringRule]:
        return self._rules

    def get_rules_for_institute(self, institute_id: str) -> List[ScoringRule]:
        return self._institute_map.get(institute_id, [])
