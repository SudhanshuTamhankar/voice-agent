from app.schemas.profile import UserProfile, GapCategory, CollegeBucket
from app.api.routes import recommendation_engine

def test_recommendation_and_gaps():
    print("Testing Stage 5: College Recommendation & Gap Analysis...")
    
    # Very strong profile
    profile_strong = UserProfile(
        category="GENERAL",
        gender="MALE",
        class_10_score=95,
        class_12_score=95,
        graduation_score=85,
        graduation_stream="ENGINEERING",
        work_ex_months=24,
        actual_percentile=99.9
    )
    
    report_strong = recommendation_engine.generate_recommendations(profile_strong)
    
    print(f"Strong colleges count: {len(report_strong.strong_colleges)}")
    print(f"Realistic colleges count: {len(report_strong.realistic_colleges)}")
    
    # We should have at least some strong/realistic colleges
    assert len(report_strong.strong_colleges) + len(report_strong.realistic_colleges) > 0, "Strong profile should have some realistic colleges"
    
    # Weak profile
    profile_weak = UserProfile(
        category="GENERAL",
        gender="MALE",
        class_10_score=60,
        class_12_score=60,
        graduation_score=60,
        graduation_stream="ENGINEERING",
        work_ex_months=0,
        actual_percentile=90.0
    )
    
    report_weak = recommendation_engine.generate_recommendations(profile_weak)
    print(f"Unlikely colleges count: {len(report_weak.unlikely_colleges)}")
    assert len(report_weak.unlikely_colleges) > 0, "Weak profile should have unlikely colleges"
    
    # Gap Analysis Check
    gap_report = report_weak.gap_report
    if gap_report:
        if gap_report.biggest_fixed_bottleneck:
            print(f"Biggest fixed bottleneck: {gap_report.biggest_fixed_bottleneck.factor_name}")
            assert gap_report.biggest_fixed_bottleneck.category == GapCategory.FIXED
        if gap_report.biggest_controllable_lever:
            print(f"Biggest controllable lever: {gap_report.biggest_controllable_lever.factor_name}")
            assert gap_report.biggest_controllable_lever.category == GapCategory.CONTROLLABLE
            
    print("All tests passed.")

if __name__ == "__main__":
    test_recommendation_and_gaps()
