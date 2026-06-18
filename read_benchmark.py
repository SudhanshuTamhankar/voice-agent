import pandas as pd
from app.core.config import BENCHMARK_PATH

try:
    df = pd.read_excel(BENCHMARK_PATH, sheet_name="Final_Master_Table")
    print("COLUMNS:")
    for col in df.columns:
        print(f"- {col}")
    
    print("\nSAMPLE ROW:")
    print(df.iloc[0].to_dict())
except Exception as e:
    print(f"Error: {e}")
