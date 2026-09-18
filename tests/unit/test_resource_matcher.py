import pytest
from backend.schemas.models import VerifiedNeed, ResourceRecord, NeedType, UrgencyLevel
from backend.agents.resource_matcher import ResourceMatcher

def test_resource_matcher_urgency_priority():
    agent = ResourceMatcher()
    
    # 2 needs
    needs = [
        VerifiedNeed(
            need_id="n1",
            source_report_ids=["r1"],
            location_text="North Site",
            coordinates=(40.0, -74.0),
            need_type=NeedType.WATER,
            quantity_estimate=100,
            urgency=UrgencyLevel.HIGH,
            verification_confidence=1.0,
            requires_human_review=False
        ),
        VerifiedNeed(
            need_id="n2",
            source_report_ids=["r2"],
            location_text="South Site",
            coordinates=(39.0, -74.0),
            need_type=NeedType.WATER,
            quantity_estimate=100,
            urgency=UrgencyLevel.CRITICAL, # Higher urgency!
            verification_confidence=1.0,
            requires_human_review=False
        )
    ]
    
    # 1 resource with limited quantity, located near North Site
    resources = [
        ResourceRecord(
            resource_id="res1",
            resource_type=NeedType.WATER,
            quantity_available=150,
            location=(40.1, -74.0), # Near n1
            status="available"
        )
    ]
    
    allocations = agent.process(needs, resources)
    
    # n2 is CRITICAL, so it should be prioritized by the ILP objective
    # even though n1 is closer to the resource.
    
    assert len(allocations) == 2
    
    n2_alloc = next(a for a in allocations if a.need_id == "n2")
    n1_alloc = next(a for a in allocations if a.need_id == "n1")
    
    assert n2_alloc.quantity_allocated == 100 # n2 gets full amount
    assert n1_alloc.quantity_allocated == 50  # n1 gets whatever is left
    assert n1_alloc.allocation_method == "ilp_optimal"
