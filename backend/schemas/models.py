from pydantic import BaseModel, Field, field_validator
from enum import Enum
from datetime import datetime
from typing import Optional, List, Tuple

class NeedType(str, Enum):
    MEDICAL = "medical"
    SHELTER = "shelter"
    WATER = "water"
    FOOD = "food"
    RESCUE = "rescue"
    OTHER = "other"

class UrgencyLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"

class RawReport(BaseModel):
    report_id: str
    source_channel: str            # "sms", "web_form", "social_media"
    raw_text: str = Field(max_length=2000)
    submitted_at: datetime
    reporter_contact: Optional[str] = None

    @field_validator('raw_text')
    def raw_text_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('raw_text cannot be empty')
        return v

def validate_coordinates(coords: Optional[Tuple[float, float]]) -> Optional[Tuple[float, float]]:
    if coords is not None:
        lat, lon = coords
        if not (-90 <= lat <= 90):
            raise ValueError(f"Latitude must be between -90 and 90. Got {lat}")
        if not (-180 <= lon <= 180):
            raise ValueError(f"Longitude must be between -180 and 180. Got {lon}")
    return coords

def validate_quantity(q: Optional[int]) -> Optional[int]:
    if q is not None and q < 0:
        raise ValueError(f"quantity_estimate cannot be negative. Got {q}")
    return q

class ExtractedNeed(BaseModel):
    report_id: str
    location_text: str
    coordinates: Optional[Tuple[float, float]] = None
    need_type: NeedType
    quantity_estimate: Optional[int] = None
    stated_urgency: UrgencyLevel
    extraction_confidence: float = Field(ge=0.0, le=1.0)

    @field_validator('coordinates')
    def validate_coords(cls, v):
        return validate_coordinates(v)

    @field_validator('quantity_estimate')
    def validate_quant(cls, v):
        return validate_quantity(v)

class VerifiedNeed(BaseModel):
    need_id: str
    source_report_ids: List[str]   # merged duplicates point back to all originals
    location_text: str
    coordinates: Optional[Tuple[float, float]] = None
    need_type: NeedType
    quantity_estimate: int
    urgency: UrgencyLevel
    verification_confidence: float = Field(ge=0.0, le=1.0)
    requires_human_review: bool
    duplicate_of: Optional[str] = None
    
    @field_validator('coordinates')
    def validate_coords(cls, v):
        return validate_coordinates(v)

    @field_validator('quantity_estimate')
    def validate_quant(cls, v):
        return validate_quantity(v)

class ResourceRecord(BaseModel):
    resource_id: str
    resource_type: NeedType
    quantity_available: int
    location: Tuple[float, float]
    status: str   # "available", "reserved", "dispatched"

    @field_validator('location')
    def validate_coords(cls, v):
        return validate_coordinates(v)

class Allocation(BaseModel):
    need_id: str
    resource_id: str
    quantity_allocated: int
    distance_km: float
    allocation_method: str   # "ilp_optimal", "greedy_fallback"

class DispatchPlan(BaseModel):
    plan_id: str
    generated_at: datetime
    allocations: List[Allocation]
    unmet_needs: List[str]         # need_ids with no allocation
    narrative: str                 # human-readable summary, grounded in the fields above only

class EvaluationResult(BaseModel):
    plan_id: str
    coverage_pct: float
    critical_unmet_count: int
    fairness_score: float
    passed: bool
    rationale: str
    revision_notes: Optional[str] = None
