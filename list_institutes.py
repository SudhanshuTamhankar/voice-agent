import pandas as pd
from app.core.config import PROFILE_SCORING_ENGINE_PATH

df = pd.read_csv(PROFILE_SCORING_ENGINE_PATH)
institutes = df["Institute_Name"].dropna().unique()
print("Institutes in CSV:")
for inst in institutes:
    print(inst)
