import pandas as pd
from typing import List, Optional
from app.core.config import BENCHMARK_PATH
from app.core.exceptions import MissingDatasetError, DatasetParsingError
from app.schemas.benchmark import Benchmark

class BenchmarkRepository:
    def __init__(self):
        self._benchmarks = []
        self._map = {}
        self._load_excel()

    def _load_excel(self):
        try:
            # Load the main master table
            df = pd.read_excel(BENCHMARK_PATH, sheet_name="Final_Master_Table")
            # Replace NaN with None for pydantic
            df = df.where(pd.notnull(df), None)
            
            for index, row in df.iterrows():
                try:
                    row_dict = row.to_dict()
                    benchmark = Benchmark(**row_dict)
                    benchmark.raw_data = row_dict  # Keep raw data for flexible access
                    self._benchmarks.append(benchmark)
                    
                    key = (benchmark.institute_id, benchmark.category.lower())
                    self._map[key] = benchmark
                except Exception as e:
                    raise DatasetParsingError(f"Error parsing row {index} in {BENCHMARK_PATH}: {e}")
        except FileNotFoundError:
            raise MissingDatasetError(f"Dataset file not found: {BENCHMARK_PATH}")
        except Exception as e:
            raise DatasetParsingError(f"Failed to read Excel file {BENCHMARK_PATH}: {e}")

    def get_all(self) -> List[Benchmark]:
        return self._benchmarks

    def get_benchmark(self, institute_id: str, category: str) -> Optional[Benchmark]:
        key = (institute_id, category.lower())
        return self._map.get(key)
