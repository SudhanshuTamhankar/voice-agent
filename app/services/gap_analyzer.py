from typing import List, Optional
from app.schemas.profile import UserProfile, ProfileGap, GapCategory, GapReport
from app.schemas.scoring import CompositeScoreResult

class ProfileGapAnalyzer:
    """
    Analyzes the factor breakdown from a CompositeScoreResult to determine where
    the user is losing points, classifying them as FIXED or CONTROLLABLE gaps.
    """
    FIXED_FACTORS = ["10th", "12th", "graduation", "gender", "category", "academic_diversity", "diversity", "academic"]
    
    @classmethod
    def analyze_gaps(cls, profile: UserProfile, result: CompositeScoreResult) -> GapReport:
        gaps: List[ProfileGap] = []
        
        for factor in result.factors:
            if factor.max_possible_score is None:
                continue
                
            points_lost = factor.max_possible_score - factor.score_awarded
            
            # If the user lost a non-trivial amount of points
            if points_lost > 0.5:
                # Determine category
                category = GapCategory.CONTROLLABLE
                factor_name_lower = factor.factor_name.lower()
                
                # Check if it's a fixed academic/demographic factor
                for fixed_key in cls.FIXED_FACTORS:
                    if fixed_key in factor_name_lower:
                        category = GapCategory.FIXED
                        break
                
                # Work experience is fixed if it's already high, or controllable if they are young
                if "work" in factor_name_lower or "experience" in factor_name_lower:
                    if profile.work_ex_months and profile.work_ex_months >= 24:
                        category = GapCategory.FIXED
                    else:
                        category = GapCategory.CONTROLLABLE
                        
                # CAT is always controllable
                if "cat" in factor_name_lower or "percentile" in factor_name_lower:
                    category = GapCategory.CONTROLLABLE
                
                desc = f"Lost {points_lost:.1f} pts out of {factor.max_possible_score:.1f} in {factor.factor_name}"
                
                gaps.append(ProfileGap(
                    factor_name=factor.factor_name,
                    category=category,
                    points_lost=points_lost,
                    description=desc
                ))
                
        # Sort gaps by points lost (descending)
        gaps.sort(key=lambda g: g.points_lost, reverse=True)
        
        # Identify biggest bottlenecks
        fixed_gaps = [g for g in gaps if g.category == GapCategory.FIXED]
        controllable_gaps = [g for g in gaps if g.category == GapCategory.CONTROLLABLE]
        
        return GapReport(
            all_gaps=gaps,
            biggest_fixed_bottleneck=fixed_gaps[0] if fixed_gaps else None,
            biggest_controllable_lever=controllable_gaps[0] if controllable_gaps else None
        )
