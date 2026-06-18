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

print("Forward Score calculation at 99.0 percentile:")
for inst_id, calc in CALCULATORS.items():
    try:
        res = calc.calculate(profile)
        # Now test reverse engineering: if we target exactly 'total_score', it should give us ~99.0 back!
        required_pct = calc.estimate_required_percentile(profile, res.total_score)
        
        if required_pct is not None:
            print(f"PASS: {inst_id}: Target={res.total_score} -> Reversed Percentile={required_pct}")
        else:
            print(f"SKIP: {inst_id}: No mathematical reverse engineering possible.")
    except Exception as e:
        print(f"FAIL: {inst_id} -> {e}")
