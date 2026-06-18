from .base_calculator import BaseCalculator
from .iima_calculator import IIMACalculator
from .iimb_calculator import IIMBCalculator
from .iimc_calculator import IIMCCalculator
from .iiml_calculator import IIMLCalculator
from .iimi_calculator import IIMICalculator
from .iimk_calculator import IIMKCalculator
from .fms_calculator import FMSCalculator
from .mdi_calculator import MDICalculator
from .iift_calculator import IIFTCalculator
from .iimsambalpur_calculator import IIMSambalpurCalculator
from .iimshillong_calculator import IIMShillongCalculator
from .generic_exam_calculator import GenericExamCalculator

# Registry of calculators
CALCULATORS = {
    "iim_ahmedabad": IIMACalculator(),
    "iim_bangalore": IIMBCalculator(),
    "iim_calcutta": IIMCCalculator(),
    "iim_lucknow": IIMLCalculator(),
    "iim_indore": IIMICalculator(),
    "iim_kozhikode": IIMKCalculator(),
    "fms_delhi": FMSCalculator(),
    "mdi_gurgaon": MDICalculator(),
    "iift_delhi": IIFTCalculator(),
    "iim_sambalpur": IIMSambalpurCalculator(),
    "iim_shillong": IIMShillongCalculator(),
    
    # Generic Exam/Opaque Institutes
    "xlri_jamshedpur": GenericExamCalculator("xlri_jamshedpur", "XLRI BM/HRM shortlists are based entirely on XAT scores without profile weightage."),
    "nmims_mumbai": GenericExamCalculator("nmims_mumbai", "NMIMS shortlists are based strictly on NMAT sectional and total scores."),
    "sibm_pune": GenericExamCalculator("sibm_pune", "SIBM Pune GE-PI shortlists are based entirely on overall SNAP percentile."),
    "jbims_mumbai": GenericExamCalculator("jbims_mumbai", "JBIMS is governed by the DTE CAP process and relies on MAH-MBA CET or equivalent exam scores."),
    "isb_hyderabad": GenericExamCalculator("isb_hyderabad", "ISB uses a holistic profile review (essays, GMAT/GRE, LORs) without a published formula."),
    "spjimr_mumbai": GenericExamCalculator("spjimr_mumbai", "SPJIMR uses an opaque profile-based and profile-cum-score-based pathway without a published formula."),
    "iim_ranchi": GenericExamCalculator("iim_ranchi", "IIM Ranchi does not publish a mathematical formula for its initial PI shortlist."),
    "iifm_bhopal": GenericExamCalculator("iifm_bhopal", "IIFM Bhopal shortlisting relies primarily on the entrance exam score without a published formula.")
}

def get_calculator(institute_id: str) -> BaseCalculator:
    return CALCULATORS.get(institute_id.lower())
