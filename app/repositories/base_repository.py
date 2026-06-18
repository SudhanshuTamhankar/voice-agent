import csv
import json
from typing import List, TypeVar, Type, Dict, Any
from pydantic import BaseModel

from app.core.exceptions import MissingDatasetError, DatasetParsingError

T = TypeVar("T", bound=BaseModel)

class BaseRepository:
    """Base repository to handle loading CSV/JSON files into Pydantic models."""
    
    @staticmethod
    def load_csv(file_path: str, model: Type[T]) -> List[T]:
        items = []
        try:
            with open(file_path, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    try:
                        items.append(model(**row))
                    except Exception as e:
                        raise DatasetParsingError(f"Error parsing row {i} in {file_path}: {e}")
        except FileNotFoundError:
            raise MissingDatasetError(f"Dataset file not found: {file_path}")
        return items

    @staticmethod
    def load_json(file_path: str, model: Type[T]) -> List[T]:
        try:
            with open(file_path, mode='r', encoding='utf-8-sig') as f:
                data = json.load(f)
                items = []
                for i, row in enumerate(data):
                    try:
                        items.append(model(**row))
                    except Exception as e:
                        raise DatasetParsingError(f"Error parsing item {i} in {file_path}: {e}")
                return items
        except FileNotFoundError:
            raise MissingDatasetError(f"Dataset file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise DatasetParsingError(f"Invalid JSON in {file_path}: {e}")
