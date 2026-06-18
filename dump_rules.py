import pandas as pd
from app.core.config import PROFILE_SCORING_ENGINE_PATH

df = pd.read_csv(PROFILE_SCORING_ENGINE_PATH)

with open("institute_rules_dump.txt", "w", encoding="utf-8") as f:
    for inst, group in df.groupby("Institute_Name"):
        f.write(f"\n{'='*40}\n{inst}\n{'='*40}\n")
        for _, row in group.iterrows():
            factor = row["Factor"]
            weight = row["Weightage"]
            form = row["Formula"]
            f.write(f"- {factor} | Weight: {weight} | Formula: {form}\n")
