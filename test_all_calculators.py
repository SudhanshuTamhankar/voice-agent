from app.services.calculators import CALCULATORS
from app.schemas.profile import UserProfile

profile = UserProfile(
    category="General",
    gender="Male",
    class_10_score=85.0,
    class_12_score=82.0,
    graduation_score=75.0,
    graduation_stream="Engineering",
    work_ex_months=24,
    target_exam="CAT",
    actual_percentile=99.0
)

print("Running all calculators...\n")
for inst_id, calc in CALCULATORS.items():
    try:
        res = calc.calculate(profile)
        print(f"PASS: {inst_id}: Score = {res.total_score}")
    except Exception as e:
        print(f"FAIL: {inst_id} -> {e}")
