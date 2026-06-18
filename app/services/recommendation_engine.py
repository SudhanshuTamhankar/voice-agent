from app.schemas.profile import UserProfile, CollegeBucket, CollegeRecommendation, RecommendationReport
from app.services.profile_scoring_engine import ProfileScoringEngine
from app.services.gap_analyzer import ProfileGapAnalyzer
from app.repositories.benchmark_repository import BenchmarkRepository
from app.services.calculators import CALCULATORS

class RecommendationEngine:
    def __init__(self, scoring_engine: ProfileScoringEngine, benchmark_repo: BenchmarkRepository):
        self.scoring_engine = scoring_engine
        self.benchmark_repo = benchmark_repo

    def generate_recommendations(self, profile: UserProfile) -> RecommendationReport:
        report = RecommendationReport()
        
        all_score_results = []
        
        # Iterate over all registered calculators
        for inst_id, calculator in CALCULATORS.items():
            # Get the deterministic score
            score_result = self.scoring_engine.calculate_score(profile, inst_id)
            all_score_results.append((inst_id, score_result))
            
            # Fetch benchmark
            benchmark = self.benchmark_repo.get_benchmark(inst_id, profile.category)
            
            if not benchmark or benchmark.composite_score_safe is None:
                report.insufficient_data_colleges.append(inst_id)
                continue
                
            safe = benchmark.composite_score_safe
            stretch = benchmark.composite_score_stretch or (safe * 0.95)
            
            total = score_result.total_score
            gap_from_safe = safe - total
            
            # Check if mathematically possible (e.g. if gap > max_possible_cat)
            # Find CAT factor
            cat_factor = next((f for f in score_result.factors if "cat" in f.factor_name.lower()), None)
            
            is_possible = True
            if cat_factor and cat_factor.max_possible_score:
                # If the score they already got PLUS the max possible CAT score they could get is STILL less than stretch
                current_score_without_cat = total - cat_factor.score_awarded
                max_possible_total = current_score_without_cat + cat_factor.max_possible_score
                if max_possible_total < stretch:
                    is_possible = False
            
            bucket = CollegeBucket.INSUFFICIENT_DATA
            
            if not is_possible:
                bucket = CollegeBucket.UNLIKELY
            elif total >= safe:
                bucket = CollegeBucket.STRONG
            elif total >= stretch:
                bucket = CollegeBucket.REALISTIC
            elif total >= (stretch * 0.90): # within 10% of stretch
                bucket = CollegeBucket.STRETCH
            elif total >= (stretch * 0.80):
                bucket = CollegeBucket.AMBITIOUS
            else:
                bucket = CollegeBucket.UNLIKELY
                
            rec = CollegeRecommendation(
                institute_id=inst_id,
                bucket=bucket,
                total_score=total,
                safe_benchmark=safe,
                gap_from_safe=gap_from_safe,
                is_mathematically_possible=is_possible
            )
            
            if bucket == CollegeBucket.STRONG:
                report.strong_colleges.append(rec)
            elif bucket == CollegeBucket.REALISTIC:
                report.realistic_colleges.append(rec)
            elif bucket == CollegeBucket.STRETCH:
                report.stretch_colleges.append(rec)
            elif bucket == CollegeBucket.AMBITIOUS:
                report.ambitious_colleges.append(rec)
            elif bucket == CollegeBucket.UNLIKELY:
                report.unlikely_colleges.append(rec)
                
        # To generate a meaningful macro gap report, we run it on the top Stretch or Realistic college.
        target_rec = None
        if report.stretch_colleges:
            target_rec = report.stretch_colleges[0]
        elif report.realistic_colleges:
            target_rec = report.realistic_colleges[0]
        elif report.ambitious_colleges:
            target_rec = report.ambitious_colleges[0]
        elif report.unlikely_colleges:
            target_rec = report.unlikely_colleges[0]
            
        if target_rec:
            # Find the ScoreResult for this specific college
            target_score_result = next(sr for inst, sr in all_score_results if inst == target_rec.institute_id)
            report.gap_report = ProfileGapAnalyzer.analyze_gaps(profile, target_score_result)
            
        return report
