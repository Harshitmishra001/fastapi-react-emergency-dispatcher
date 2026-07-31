from typing import TypedDict, Optional, List
from backend.schemas.models import RawReport, ExtractedNeed, VerifiedNeed, Allocation, DispatchPlan, EvaluationResult, ResourceRecord

class CoordinatorState(TypedDict):
    raw_report: RawReport
    extracted_need: Optional[ExtractedNeed]
    verified_need: Optional[VerifiedNeed]
    
    # Context data needed for matching
    existing_needs: List[VerifiedNeed]
    available_resources: List["ResourceRecord"] # String typed to avoid circular import if needed, but we can import it.
    
    allocations: Optional[List[Allocation]]
    plan: Optional[DispatchPlan]
    evaluation: Optional[EvaluationResult]
    
    revision_count: int
    requires_human_review: bool
