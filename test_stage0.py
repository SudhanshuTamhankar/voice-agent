import sys
import os
from pathlib import Path

# Add project root to path so 'app' can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent))

def main():
    try:
        from app.repositories import (
            InstituteRepository,
            FactorRepository,
            ScoringRuleRepository,
            BenchmarkRepository,
            KnowledgeBaseRepository
        )
        
        print("Testing InstituteRepository...")
        inst_repo = InstituteRepository()
        print(f"Loaded {len(inst_repo.get_all())} institutes.")
        
        print("Testing FactorRepository...")
        factor_repo = FactorRepository()
        print(f"Loaded {len(factor_repo.get_all())} factors.")
        
        print("Testing ScoringRuleRepository...")
        rule_repo = ScoringRuleRepository()
        print(f"Loaded {len(rule_repo.get_all())} scoring rules.")
        
        print("Testing KnowledgeBaseRepository...")
        kb_repo = KnowledgeBaseRepository()
        print(f"Loaded {len(kb_repo.get_all())} KB entries.")
        
        print("Testing BenchmarkRepository...")
        bench_repo = BenchmarkRepository()
        print(f"Loaded {len(bench_repo.get_all())} benchmark entries.")
        
        print("\nAll repositories loaded successfully! Stage 0 MVP is complete.")
        
    except Exception as e:
        print(f"FAILED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
